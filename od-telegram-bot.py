# Import regex, json, os and logging modules from standard library
import re, json, logging, requests, importlib, sys, os
from threading import Thread

# Import modules from python-telegram-bot
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters,
                          ConversationHandler)

# Import JSONlogic to parse the logic in Open Decision data format
from json_logic import jsonLogic
# To convert html formatted text from the Open Decision data format to Markdown text
import html2text

from utils.get_strings import get_strings as _
import utils.admin

import utils.user_menu
import settings.settings as settings

from utils.utils import send_typing_action, user_is_admin, restricted

# Set up instance of html2text and enable unicode
text2markup = html2text.HTML2Text()
text2markup.unicode_snob = True

# Set up the logging module, change level=logging.INFO to level=logging.DEBUG to reveive extended debug information
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define possible states
MAIN_MENU, CHECK_ANSWER, ADMIN_TOOLS = range(3)

# Define callback functions
@send_typing_action
def start(update, context):
    if _('welcome_message'):
        update.effective_message.reply_text(_('welcome_message'), parse_mode=ParseMode.MARKDOWN)
    if settings.GREET_IMAGE != '':
        try:
            update.effective_message.reply_photo(photo=settings.GREET_IMAGE)
        except:
            pass
    start_query = context.args[0] if context.args and len(context.args) != 0 else ''
    if re.match("^[a-z]{10}$", start_query):
        context.chat_data['start_query'] = start_query
        return load_tree(update, context)
    else:
        if user_is_admin(update):
            update.effective_message.reply_text('You are an Admin of this bot! Click /settings to edit the settings of your bot.', parse_mode=ParseMode.MARKDOWN)
        return utils.user_menu.main_menu(update, context)

# Load the query using the provided access code from the Open Decision builder instance
def load_tree(update, context):
    start_query = context.chat_data['start_query']
    r = requests.get(settings.OD_URL + '/ajax/get_published_tree/?selected_tree=' + start_query)
    if r.status_code == 200:
        tree = json.loads(r.text)
        context.chat_data['tree'] = tree
        context.chat_data['current_node'] = tree['header']['start_node']
        context.chat_data['log'] = {'nodes': [], 'answers': {}}
        update.effective_message.reply_text(
        _('tree_found').format(tree['header']['tree_name']),
        parse_mode=ParseMode.MARKDOWN)
        return display_node (update, context)

    #If the request fails due to an improperly formated access code
    elif r.status_code == 400:
        update.effective_message.reply_text(
        _('access_key_invalid_format'),
        parse_mode=ParseMode.MARKDOWN)
        context.chat_data['menu_log'].pop()
        return MAIN_MENU

    #If the request fails as no tree matches the access code
    elif r.status_code == 404:
        update.effective_message.reply_text(
        _('tree_not_found'),
        parse_mode=ParseMode.MARKDOWN)
        context.chat_data['menu_log'].pop()
        return MAIN_MENU

# Gather the data of the current node/question and send it to the user
@send_typing_action
def display_node (update, context):
    current_node = context.chat_data['current_node']
    tree = context.chat_data['tree']

    # If the inputs array/list is empty, the query is ending at that node
    if len(tree[current_node]['inputs']) == 0:
        if tree[current_node]['text'] != '':
            message = text2markup.handle(tree[current_node]['text'])
            update.effective_message.reply_text(message, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN)
        return end (update, context)

    # Show the input elements according to the input type
    for i in tree[current_node]['inputs']:

        # Show a custom keyboard with the provided answer options
        if i['type'] == 'button':
            reply_keyboard = ReplyKeyboardMarkup([i['options']], one_time_keyboard=True)
            if tree[current_node]['text'] != '':
                message = text2markup.handle(tree[current_node]['text'])
                update.effective_message.reply_text(message, reply_markup=reply_keyboard, parse_mode=ParseMode.MARKDOWN)

        # Telegram has select/dropdown equivalent, display a list of options with numbers as selectors for the user instead
        elif i['type'] == 'list':
            option_string = ''
            for idx, o in enumerate(i['options']):
                option_string += f'{idx + 1}: {o}<br>'

            if tree[current_node]['text'] != '':
                message = text2markup.handle(tree[current_node]['text'])
                update.effective_message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            update.effective_message.reply_text(text2markup.handle(option_string), reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN)

        elif((i['type'] == 'number') or (i['type'] == 'free_text')):
            if tree[current_node]['text'] != '':
                message = text2markup.handle(tree[current_node]['text'])
                update.effective_message.reply_text(message, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN)

    return CHECK_ANSWER

# Evaluate the user's answer and decide where to go next
@send_typing_action
def check_answer (update, context):

    # Fixes a bug where the state change doesn't take effect at the end of a query
    if 'tree' not in context.chat_data:
        return end(update, context)
    current_node = context.chat_data['current_node']
    tree = context.chat_data['tree']
    log = context.chat_data['log']

    #Get answer and format it according to the input-type
    answer = str(update.message.text)
    input_type = tree[current_node]['inputs'][0]['type']
    if input_type == 'list':
        try:
            index = int(answer) - 1
            answer = tree[current_node]['inputs'][0]['options'][index]
        except (IndexError, ValueError):
            update.effective_message.reply_text(_('invalid_number_list'))
            display_node (update, context)
    elif input_type == 'button':
        answer = tree[current_node]['inputs'][0]['options'].index(answer)
        answer = str(answer)
    elif input_type == 'number':
        try:
            answer = float(answer.replace(',','.'))
        except ValueError:
            update.effective_message.reply_text(_('invalid_number'))
            display_node (update, context)

    #Use jsonLogic to parse the logic block of the node
    log['nodes'].append(current_node)
    log['answers'][current_node] = answer
    if (len(tree[current_node]['rules'].items()) == 0):
        if 'default' in tree[current_node]['destination']:
            # If short text
            current_node = tree[current_node]['destination']['default']
        else:
            # If only buttons
            current_node = tree[current_node]['destination'][answer]
    else:
      #If we have rules
        rule = jsonLogic(tree[current_node]['rules'], {"a":answer})
        current_node = tree[current_node]['destination'][rule]

    #Save values back to the context object and call display node to show the next query
    context.chat_data['current_node'] = current_node
    context.chat_data['log'] = log
    display_node(update, context)

# Handler called after a query finished
def end (update, context):
    update.effective_message.reply_text(_('end_of_query'))
    context.chat_data.clear()
    return MAIN_MENU

# Handler to restart a given query
def restart(update, context):
    tree = context.chat_data['tree']
    update.effective_message.reply_text(_('restart_query'), reply_markup=ReplyKeyboardRemove())
    context.chat_data['current_node'] = tree['header']['start_node']
    context.chat_data['log'] = {'nodes': [], 'answers': {}}
    return display_node(update, context)

# Handler to go a step/question back during a query to e.g. change an answer
def back(update, context):
    update.effective_message.reply_text(_('go_back'), reply_markup=ReplyKeyboardRemove())
    if len(context.chat_data['log']['nodes']) > 0:
        context.chat_data['current_node'] = context.chat_data['log']['nodes'][-1]
        context.chat_data['log']['answers'].pop(context.chat_data['log']['nodes'][-1], None)
        context.chat_data['log']['nodes'].pop()
    return display_node(update, context)

def reload_settings():
    importlib.reload(settings)

# Log Errors caused by Updates
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(settings.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    @restricted
    def reboot(update, context):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()


    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MAIN_MENU : [CallbackQueryHandler(utils.user_menu.check_query), CommandHandler('new', start), CommandHandler('settings', utils.admin.admin_settings), MessageHandler(Filters.text, utils.user_menu.check_input)],

            CHECK_ANSWER: [CommandHandler('restart', restart), CommandHandler('back', back), CommandHandler('menu', start), MessageHandler(Filters.text, check_answer)],

            ADMIN_TOOLS : [CallbackQueryHandler(utils.admin.check_query), CommandHandler('reboot', reboot), MessageHandler(Filters.text, utils.admin.check_input)]

        },
        fallbacks=[CommandHandler('end', end)],
    )

    dp.add_handler(conv_handler)

    # Log all errors. Commenting out this line will make the bot script stop complety if an error occurs but provides the full python error trace.
    #If enabled, there will be extended telegram data on the update that caused the error, but no python error trace.

    #dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
