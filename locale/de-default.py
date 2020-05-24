## Start
# Welcome message - It's sent when the user contacts the bot the first time
welcome_message = "Herzlich willkommen! Ich bin der Open-Decision-Bot, ich bin hier, um Sie um Bäume von [Open-Decision.org](https://open-decision.org) abzufragen."


# Main Menu Buttons
# Available queries Button - Label of the menu button to show the available queries if queries were set by the admin
available_queries_button = 'Was kannst du?'

# Access Code Button - Label of the menu button to enter an access code
access_code_button = 'Ich habe einen Zugangscode'

# Demo Button - Label of the menu button to start the demo if a demo was was set by the admin
demo_button = 'Zeig mir ein Beispiel'

# Know More Button - Label of the menu button show the info message containing additional information regarding the bot etc
info_button = 'Wer bist du?'

# Change Language Button - Label of the menu button to change the language
change_language_button = 'Sprache ändern'

# Back Button - System-wide button to go back within menus
back_button = '<< Zurück'

# Main Menu Messages
# Main Menu Message - The message above the main menu asking what the user wants to do e.g. 'What do you want to do?'
main_menu_message = 'Wie kann ich dir heute helfen?'

# Query List Message - The message above the list of available queries
query_list_message = 'Bei diesen Themen kann ich dir helfen'

# Select Language Message - The message above choice of languages
select_language_message = 'In welcher Sprache soll ich mit dir Sprechen?'

# Bot Info - Sent when the user clicks the 'Know More' button in the main menu. Explain what your bot is doing, or who you are.
bot_info = 'Ich bin ein cooler Bot.'

## Starting the query
# Ask for access code - Asks the user to enter the access code of an tree or click the special link to start the query.
enter_access_code = 'Bitte geben Sie Ihren Zugangscode ein oder klicken Sie auf den Link, den Sie erhalten haben.'

# Tree found - Sent if the tree matching the access code was found and the query starts. By default, the user is also told about the navigation using /back, /restart and /menu. Enter {} where the name of the query should be displayed.
tree_found = 'Großartig, die Abfrage {} wird jetzt gestartet. Verwenden Sie /back oder /restart, um einen Schritt zurück zu gehen oder die Abfrage neu zu starten und /menu, um zum Hauptmenü zurückgehen.'

# Invalid Access Key Format  - Sent if the provided access key has an invalid format
access_key_invalid_format = 'Dieser Zugangscode hat kein gültiges Format. Bitte verwenden Sie den richtigen Link oder Code für Ihren Baum.'

# Tree not found - Sent if the access key was in the right format but the tree wasn't found on the server running the builder
tree_not_found = 'Der von Ihnen angeforderte Baum wurde nicht gefunden. Bitte geben Sie einen neuen Code ein.'

## During the query
# Invalid Number - Sent if the user was asked to enter a number but send e.g. text instead
invalid_number = 'Bitte geben Sie eine gültige Zahl ein.'

# Invalid list choice - Sent if the user was asked to select an item from a list but sent a choice that's not available
invalid_number_list = 'Bitte geben Sie eine gültige Zahl aus der Liste ein.'

# Restart - Sent if the query is restarted
restart_query = 'Okay, der Bot wird neu gestartet.'

# Go back - Sent if the users goes a step back within a query
go_back = 'Okay, ich werde einen Schritt zurückgehen.'

# End Message - Sent after the user finishes a query
end_of_query = 'Danke, dass Sie den Bot benutzen! Klicken Sie auf /menu, um neu zu starten.'

## Errors
# Error Message - Sent if a message could not be found
not_found = 'Es tut mir leid, ich habe leider einen Fehler gemacht. Bitte gehe zurück.'
