from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
#  Mögliche States werden definiert
AUSWAHL, HOEHE, WISSEN, NACHRICHT, SCHREIBEN, ENDE = range(6)

forderung = 0
# Hauptmenü des Bots
def start(bot, update):
    reply_keyboard = [['Ruecklastschriftgebuehren', 'Miete', 'Mit Dir']]

    update.message.reply_text(
        'Hi, wilkommen bei der Alpha-Version des HCLC-Bots! '
        'Womit hast du ein Problem?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return AUSWAHL
# Abfrage der Gebuehren
def gebuehren(bot, update):
    update.message.reply_text('Wie viel Gebuehren sollst du wegen der Ruecklastschrift bezahlen?')
    return HOEHE

# Berechnung, ob die geforderten Gebühren zu hoch sind
def zu_hoch(bot, update):
    reply_keyboard = [['Ja', 'Nein']]
    global forderung
    forderung = update.message.text
    if is_number(forderung):
        forderung = float(forderung)
        if 4 < forderung:
            update.message.reply_text('Das ist aber viel!'
            ' War die Lastschrift denn vorher durch eine Rechnung angekuendigt oder zieht die Firma regelmaessig Geld ein (z.B. Netflix-Abo)?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return WISSEN
        else:
            update.message.reply_text('Bis vier Euro sind leider in Ordnung. Schreibe /cancel um neuzustarten.')
            return
    else:
        update.message.reply_text('Bitte gib eine Zahl ein. Benutze als Trennzeichen bitte einen Punkt und kein Komma.')
        gebuehren()

# Abfrage des Mahnweges
def gewusst(bot, update):
    reply_keyboard = [['Brief', 'SMS', 'E-Mail', 'Garnicht']]
    update.message.reply_text('Okay, noch eine Frage.'
    ' Wie wurdest du nach der fehlgeschlagenen Lastschrift benachrichtigt?',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return NACHRICHT

# Berechnung mögl. Porto und Materialkosten je nach Mahnweg, Ausgabe des Ergebnis
def einsparung(bot, update):
    reply_keyboard = [['Ja', 'Nein']]
    antwort = update.message.text
    if antwort == 'Brief':
        zulaessige_gebuehren = 4
    elif antwort == 'SMS':
        zulaessige_gebuehren = 3.09
    elif antwort == 'E-Mail':
        zulaessige_gebuehren = 3
    elif antwort == 'Garnicht':
        zulaessige_gebuehren = 3
    gespart = forderung - zulaessige_gebuehren
    update.message.reply_text('Glueckwunsch! Du sollstest %02d EUR bezahlen, allerdings sind in deinem Fall nur %02d EUR zulaessig. Du kannst also %02d EUR sparen! Soll ich dir ein Musterschreiben generieren?' % (forderung, zulaessige_gebuehren, gespart), reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return SCHREIBEN

# Ausgabe des Schreibens an den Gläubiger
def print_schreiben (bot, update):
    update.message.reply_text("Die pauschale Absetzung von Ruecklastschriftgebuehren...")
    ende(bot, update)

#Ende der Beratung
def ende (bot, update):
    update.message.reply_text("Danke, dass du den Botvokat benutzt hast! Schreibe /cancel um neuzustarten")

# Musterschreiben bei Lastschrift-Abbuchung ohne Ankündigung -> nicht erlaubt
def nicht_gewusst(bot, update):
    update.message.reply_text('Oh oh, das geht aber nicht. Schicke folgenden Text an die Firma: <Musterschreiben>. Schreibe /cancel um neuzustarten')
    return ENDE

# Man ist halt auch nur ein Mensch
def miete(bot, update):
    update.message.reply_text('Das kann ich leider noch nicht, aber ich lerne jeden Tag dazu. Schreibe /cancel um neuzustarten')
    return ENDE

# Cause Hide the pain Harold is the best
def gangsta(bot, update):
    update.message.reply_text('Cool. '
    'Schreibe /cancel um neuzustarten.')
    update.message.reply_photo(photo=open('test.jpeg', 'rb'))
    return ENDE

# Check if entered value is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("------")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            AUSWAHL: [RegexHandler('^Ruecklastschriftgebuehren$', gebuehren),
                    RegexHandler('^Miete$', miete),
                    RegexHandler('^Mit Dir$', gangsta)],

            HOEHE: [MessageHandler(Filters.text, zu_hoch)],

         WISSEN: [RegexHandler('^Ja$', gewusst),
                RegexHandler('^Nein$', nicht_gewusst)],


         NACHRICHT: [MessageHandler(Filters.text, einsparung)],

            SCHREIBEN: [RegexHandler('^Ja$', print_schreiben),
                   RegexHandler('^Nein$', ende)],
        },

        fallbacks=[CommandHandler('cancel', start)]
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
