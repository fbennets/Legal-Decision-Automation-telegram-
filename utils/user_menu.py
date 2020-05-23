# Import regex and importlib from standard library
import re, importlib

# Import modules from python-telegram-bot
from telegram import (ParseMode, InlineKeyboardButton, InlineKeyboardMarkup)

from utils.get_strings import get_strings as _

from utils.utils import send_typing_action, build_menu

from utils.user_menu_data import user_menu_data as menu_data
import settings.settings as settings

main = importlib.import_module('od-telegram-bot')

MAIN_MENU, CHECK_ANSWER, ADMIN_TOOLS = range(3)


def main_menu(update,context):
    context.chat_data['menu_log'] = []
    context.chat_data['current_menu_step'] = 'start'
    return show_inline_menu(update, context, 'input')

@send_typing_action
def show_inline_menu(update, context, before, feedback_message = None):
    query = update.callback_query
    current_menu_step = context.chat_data['current_menu_step']

    message = ""

    if current_menu_step == 'start':
        message += _('main_menu_message')

        button_list = []
        cols = 2
        if settings.QUERY_LIST != ['']:
            button_list.append(InlineKeyboardButton(_('available_queries_button'), callback_data='show_queries'))

        button_list.append(InlineKeyboardButton(_('access_code_button'), callback_data='enter_access_code'))

        if settings.DEMO_QUERY:
             button_list.append(InlineKeyboardButton(_('demo_button'), callback_data='start_demo'))

        button_list.append(InlineKeyboardButton(_('info_button'), callback_data='know_more'))

        if settings.allow_language_change == True:
            button_list.append(InlineKeyboardButton(_('change_language_button'), callback_data='change_language'))

    elif current_menu_step == 'show_queries':
        message += _('query_list_message')
        button_list = [InlineKeyboardButton(query[0], callback_data=query[1]) for query in settings.QUERY_LIST]
        button_list.append(InlineKeyboardButton(_('back_button'), callback_data='back'))
        cols = 1

    elif current_menu_step == 'enter_access_code':
        message += _('enter_access_code')
        button_list = [InlineKeyboardButton(_('back_button'), callback_data='back')]
        cols = 2

    elif current_menu_step == 'start_demo':
        query.edit_message_reply_markup(None)
        context.chat_data['start_query'] = settings.DEMO_QUERY
        return main.load_tree(update, context)

    elif current_menu_step == 'know_more':
        message += _('bot_info')
        button_list = [(InlineKeyboardButton(_('back_button'), callback_data='back'))]
        cols = 2

    elif current_menu_step == 'change_language':
        message += _('select_language_message')
        button_list = [InlineKeyboardButton(button, callback_data=idx) for idx, button in ([('Deutsch', 'de'), ('English', 'en')])]
        button_list.append(InlineKeyboardButton(_('back_button'), callback_data='back'))
        cols = 2

    else:
        button_list = [InlineKeyboardButton(button, callback_data=idx) for idx, button in enumerate(menu_data[current_menu_step]['answers'])]
        cols = 2

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=cols))

    if before == 'input':
        if feedback_message:
            message = f'{feedback_message}\n{message}'
        update.message.reply_text(message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    elif before == 'menu':
        query.edit_message_text(text=message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    return MAIN_MENU

@send_typing_action
# Entry point if the user used the menu
def check_query(update, context):
    query = update.callback_query
    query.answer()
    current_menu_step = context.chat_data['current_menu_step']
    context.chat_data['menu_log'].append(current_menu_step)

    answer = query.data

    if answer == 'back':
        print(context.chat_data['menu_log'])
        current_menu_step = context.chat_data['menu_log'][-2]
        context.chat_data['menu_log'][:2]
        print(current_menu_step)
        context.chat_data['current_menu_step'] = current_menu_step
        return show_inline_menu(update, context, 'menu')

    elif current_menu_step == 'start':
        current_menu_step = answer
        context.chat_data['current_menu_step'] = current_menu_step
        return show_inline_menu(update, context, 'menu')

    elif current_menu_step == 'show_queries':
        context.chat_data['start_query'] = query.data.strip()
        return main.load_tree(update, context)

    elif current_menu_step == 'change_language':
        context.chat_data['current_menu_step'] = 'start'
        return show_inline_menu(update, context, 'menu')

    else:
        answer = int(query.data)
        current_menu_step = menu_data[current_menu_step]['logic'][answer]
        context.chat_data['current_menu_step'] = current_menu_step
        return show_inline_menu(update, context, 'menu')


# Entry point if the user sent message
def check_input(update, context):
    print(update.message.text)
    start_query = str(update.message.text).strip()
    if re.match("^[a-z]{10}$", start_query):
        context.chat_data['start_query'] = start_query
        return main.load_tree(update, context)
    else:
        show_inline_menu(update, context, 'input', _('tree_not_found'))


def reload_settings():
    importlib.reload(settings)
