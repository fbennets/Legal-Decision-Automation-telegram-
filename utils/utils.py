from functools import wraps
from telegram import ChatAction
import importlib, requests

import settings.settings as settings

LIST_OF_ADMINS = settings.ADMINS

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func

    return decorator

send_typing_action = send_action(ChatAction.TYPING)
send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_name = update.effective_user.username
        if user_name not in LIST_OF_ADMINS:
            return
        return func(update, context, *args, **kwargs)
    return wrapped

def user_is_admin(update):
    user_name = update.effective_user.username
    if user_name in LIST_OF_ADMINS:
        return True
    else:
        return False

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def reload_settings():
    importlib.reload(settings)

def test_image(path):
    try:
        r = requests.head(path)
        if (r.headers['Content-Type'] == 'image/png') or (r.headers['Content-Type'] == 'image/jpg') or (r.headers['Content-Type'] == 'image/jpeg'):
            return r.status_code == requests.codes.ok
        else:
            raise IndexError
    except:
        False
