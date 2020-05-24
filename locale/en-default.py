## Start
# Welcome message - It's sent when the user contacts the bot the first time
welcome_message = "Welcome! I am the Open Decision Bot, I'm here to ask you trees from [Open-Decision.org](https://open-decision.org)"


## Main Menu Buttons
# Available queries Button - Label of the menu button to show the available queries if queries were set by the admin
available_queries_button = 'Show available queries'

# Access Code Button - Label of the menu button to enter an access code
access_code_button = 'Enter access code'

# Demo Button - Label of the menu button to start the demo if a demo was was set by the admin
demo_button = 'Start Demo'

# Know More Button - Label of the menu button show the info message containing additional information regarding the bot etc
info_button = 'Know More'

# Change Language Button - Label of the menu button to change the language
change_language_button = 'Change Language'

# Back Button - System-wide button to go back within menus
back_button = '<< Back'

## Main Menu Messages
# Main Menu Message - The message above the main menu asking what the user wants to do e.g. 'What do you want to do?'
main_menu_message = 'What do you want to do?'

# Query List Message - The message above the list of available queries
query_list_message = 'These queries are available'

# Select Language Message - The message above choice of languages
select_language_message = 'Select one of the languages'

# Bot Info - Sent when the user clicks the 'Know More' button in the main menu. Explain what your bot is doing, or who you are.
bot_info = 'I am a cool bot.'

## Starting the query
# Ask for access code - Asks the user to enter the access code of an tree or click the special link to start the query.
enter_access_code = 'Please enter your Access Code or click the link you received.'

# Tree found - Sent if th treee matching the access code was found and the query starts. By default, the user is also told about the navigation using /back, /restart and /menu. Enter {} where the name of the query should be displayed.
tree_found = 'Great, the query {} will start now. Use /back or /restart to go a step back or restart the query and /menu to return to the main menu.'

# Invalid Access Key Format  - Sent if the provided access key has an invalid format
access_key_invalid_format = 'This Access Code is not in a valid format. Please use the right link or code for your tree.'

# Tree not found - Sent if the access key was in the right format but the tree wasn't found on the server running the builder
tree_not_found = 'The tree you requested was not found. Please enter a new code.'


## During the query
# Invalid Number - Sent if the user was asked to enter a number but send e.g. text instead
invalid_number = 'Please enter a valid number.'

# Invalid list choice - Sent if the user was asked to select an item from a list but sent a choice that's not available
invalid_number_list = 'Please enter a valid number from the list.'

# Restart - Sent if the query is restarted
restart_query = 'Okay, the bot will restart.'

# Go back - Sent if the users goes a step back within a query
go_back = 'Okay, I will go a step back.'

# End Message - Sent after the user finishes a query
end_of_query = 'Thanks for using the bot! Click /menu to restart.'

## Errors
# Error Message - Sent if a message could not be found
not_found = 'I am so sorry but something went wrong. Please go back.'
