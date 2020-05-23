import importlib
import ..settings

def import_strings():
    global strings
    try:
        strings = importlib.import_module('..locale.{}'.format(settings.LANG))
    except ModuleNotFoundError:
        strings = importlib.import_module('..locale.{}'.format('en'))
    global default_strings
    try:
        default_strings = importlib.import_module('..locale.{}-default'.format(settings.LANG))
    except ModuleNotFoundError:
        default_strings = importlib.import_module('..locale.{}-default'.format('en'))


def get_strings (key):
    try:
        str = getattr(strings, key)
        if str != '':
            return str
        else:
            raise AttributeError
    except AttributeError:
        try:
            str = getattr(default_strings, key)
            return str
        except AttributeError:
            return get_strings('not_found')

def reload_messages():
    importlib.reload(settings)
    importlib.reload(strings)
    importlib.reload(default_strings)
    import_strings()

import_strings()
