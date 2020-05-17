import re, json, os
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)
import logging

from json_logic import jsonLogic
import html2text
import requests

text2markup = html2text.HTML2Text()
text2markup.unicode_snob = True

TOKEN = os.environ['OD_BOT_TOKEN']
OD_URL = os.environ.get('OD_BOT_URL', 'https://builder.open-decision.org')
DEMO_QUERY = os.environ.get('OD_BOT_DEMO_QUERY')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define possible states
CHECK_ACCESS_CODE, CHECK_ANSWER = range(2)

def start(update, context):
    start_query = context.args[0] if len(context.args) != 0 else ''
    if re.match("^[a-z]{10}$", start_query):
        context.chat_data['start_query'] = start_query
        return load_tree(update, context)
    else:
        message = 'Please enter your Access Code or click the link you received.'
        if DEMO_QUERY:
            message += ' Click or type /demo, to see a demo query.'
        update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        return CHECK_ACCESS_CODE

def check_access_code(update, context):
    start_query = str(update.message.text)
    if re.match("^[a-z]{10}$", start_query):
        context.chat_data['start_query'] = start_query
        return load_tree(update, context)
    else:
        message = 'Please enter your Access Code or click the link you received.'
        if DEMO_QUERY:
            message += ' Click or type /demo, to see a demo query.'
        update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        return CHECK_ACCESS_CODE

def load_tree(update, context):
    start_query = context.chat_data['start_query']
    r = requests.get(OD_URL + '/ajax/get_published_tree/?selected_tree=' + start_query)
    if r.status_code == 200:
        tree = json.loads(r.text)
        context.chat_data['tree'] = tree
        context.chat_data['current_node'] = tree['header']['start_node']
        context.chat_data['log'] = {'nodes': [], 'answers': {}}
        update.message.reply_text(
        'Great, the query will start now. Use /back or /restart to go a step back or restart the query.',
        parse_mode=ParseMode.MARKDOWN)
        return display_node (update, context)
    #If the request fails
    elif r.status_code == 400:
        update.message.reply_text(
        'This Access Code is not in a valid format. Please use the right link or code for your tree.',
        parse_mode=ParseMode.MARKDOWN)
        return CHECK_ACCESS_CODE
    elif r.status_code == 404:
        update.message.reply_text(
        'The tree you requested was not found. Please enter a new code.',
        parse_mode=ParseMode.MARKDOWN)
        return CHECK_ACCESS_CODE

def display_node (update, context):
    current_node = context.chat_data['current_node']
    tree = context.chat_data['tree']

    if len(tree[current_node]['inputs']) == 0:
        string = text2markup.handle(tree[current_node]['text'])
        update.message.reply_text(string, parse_mode=ParseMode.MARKDOWN)
        return end (update, context)

    for i in tree[current_node]['inputs']:
        if i['type'] == 'button':
            reply_keyboard = ReplyKeyboardMarkup([i['options']], one_time_keyboard=True)
            string = text2markup.handle(tree[current_node]['text'])
            update.message.reply_text(string, reply_markup=reply_keyboard, parse_mode=ParseMode.MARKDOWN)

        elif i['type'] == 'list':
            option_string = ''
            for idx, o in enumerate(i['options']):
                option_string += f'{idx + 1}: {o}<br>'

            update.message.reply_text(text2markup.handle(tree[current_node]['text']),parse_mode=ParseMode.MARKDOWN)
            update.message.reply_text(text2markup.handle(option_string), parse_mode=ParseMode.MARKDOWN)

        elif((i['type'] == 'number') or (i['type'] == 'free_text')):
            string = text2markup.handle(tree[current_node]['text'])
            update.message.reply_text(string, parse_mode=ParseMode.MARKDOWN)

    context.chat_data['current_node'] = current_node
    return CHECK_ANSWER


def check_answer (update, context):
    if 'tree' not in context.chat_data:
        return end(update, context)
    current_node = context.chat_data['current_node']
    tree = context.chat_data['tree']
    log = context.chat_data['log']
    #Get answer
    answer = str(update.message.text)
    type_path = tree[current_node]['inputs'][0]['type']
    if type_path == 'list':
        index = int(answer) - 1
        answer = tree[current_node]['inputs'][0]['options'][index]
    elif type_path == 'button':
        answer = tree[current_node]['inputs'][0]['options'].index(answer)
        answer = str(answer)
    elif type_path == 'number':
        try:
            answer = float(answer.replace(',','.'))
        except ValueError:
            update.message.reply_text('Please enter a valid number.')

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
    #Save values back
    context.chat_data['current_node'] = current_node
    context.chat_data['log'] = log
    display_node(update, context)

def demo(update, context):
    if DEMO_QUERY:
        context.chat_data['start_query'] = DEMO_QUERY
        return load_tree(update, context)
    else:
        return check_access_code(update, context)

def end (update, context):
    update.message.reply_text('Danke, dass du den Bot benutzt hast! Klicke auf /new, um neuzustarten.')
    context.chat_data.clear()
    return CHECK_ACCESS_CODE

def restart(update, context):
    tree = context.chat_data['tree']
    update.message.reply_text('Okay, the bot will restart.', reply_markup=ReplyKeyboardRemove())
    context.chat_data['current_node'] = tree['header']['start_node']
    context.chat_data['log'] = {'nodes': [], 'answers': {}}
    return display_node(update, context)

def back(update, context):
    update.message.reply_text('Okay, I will go a step back.', reply_markup=ReplyKeyboardRemove())
    if len(context.chat_data['log']['nodes']) > 0:
        context.chat_data['current_node'] = context.chat_data['log']['nodes'][-1]
        context.chat_data['log']['answers'].pop(context.chat_data['log']['nodes'][-1], None)
        context.chat_data['log']['nodes'].pop()
    return display_node(update, context)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHECK_ANSWER: [CommandHandler('restart', restart), CommandHandler('back', back), CommandHandler('new', start), MessageHandler(Filters.text, check_answer)],
            CHECK_ACCESS_CODE : [CommandHandler('demo', demo), CommandHandler('new', start), MessageHandler(Filters.text, check_access_code)]
        },
        fallbacks=[CommandHandler('end', end)],
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
