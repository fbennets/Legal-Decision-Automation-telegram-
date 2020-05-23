
admin_menu_data = {
  'start' : {
    'text': 'What do you want to do?',
    'type': 'select',
    'answers': ['Edit Messages', 'Edit Demo', 'Edit Image', 'Change Language', 'Set available Queries', 'Reboot Bot','Exit Settings'],
    'logic':{
      0: 'edit_messages',
      1: 'edit_demo',
      2: 'edit_image',
      3: 'change_language',
      4: 'available_queries',
      5: 'reboot_bot',
      6: 'exit_settings'
    } 
  },
  'edit_messages': {
    'text': 'Please select the message you want to edit.',
    'type': 'select',
    'answers': ['Welcome Message', 'End Message', 'Asking for Access Code', '<< Back', 'Exit settings'],
    'logic':{
      0: 'welcome_message',
      1: 'end_message',
      2: 'asking_for_access_code',
      3: 'start',
      4: 'exit_settings'
    } 
  },

   'edit_demo': {
    'text': "Okay, enter the code for your demo query.",
    'type': 'input',
    'value': 'env',
    'var': 'DEMO_QUERY',
    'success': 'Okay, the demo query was set to: ',
    'answers': ['<< Back'],
    'logic':{
      0: 'input_back'
    }
  },

   'welcome_message': {
    'text': "Okay, enter your new welcome message, which is the first message that is send to the user.",
    'type': 'input',
    'value': 'message',
    'var': 'welcome_message',
    'success': 'Okay, the welcome message was set to: ',
    'answers': ['<< Back'],
        'logic':{
      0: 'input_back'
    }
  },

   'end_message': {
    'text': "Okay, enter your new end message, which is shown, after the user finished a query.",
    'type': 'input',
    'value': 'message',
    'var': 'end_message',
    'success': 'Okay, the end message was set to: ',
    'answers': ['<< Back'],
    'logic':{
      0: 'input_back'
    }
  },

   'change_language': {
    'text': "Enter either de for German or en for English or to a custom language, if you created your own language file. If no language file is found, English will be used as default.",
    'type': 'input',
    'value': 'env',
    'var': 'LANG',
    'success': 'Okay, the language was set to: ',
    'answers': ['<< Back'],
        'logic':{
      0: 'input_back'
    }
   },

'available_queries': {
    'text': "Okay, send me the queries the user should be able to select. Please use this format: \n\nQuery Name - AccessCode\nExample:\nFine Contradiction - habbiovzxa",
    'type': 'input',
    'value': 'env',
    'var': 'QUERY_LIST',
    'success': 'Okay, the available queries were set. ',
    'answers': ['<< Back'],
        'logic':{
      0: 'input_back'
    }
   },

'asking_for_access_code': {
    'text': "Okay, enter your new message to ask for the access code. The user is asked this, if no correct tree identifier is provided initially.",
    'type': 'input',
    'value': 'message',
    'var': 'enter_access_code',
    'success': 'Okay, the access code message was set to: ',
    'answers': ['<< Back'],
        'logic':{
      0: 'input_back'
    }
  },

'edit_image': {
    'text': "Please send me the full URL to your PNG or JPG image. Example: https://www.example.com/my-image.png.",
    'type': 'input',
    'value': 'env',
    'var': 'GREET_IMAGE',
    'success': 'Okay, the image was set to: ',
    'answers': ['<< Back'],
    'logic':{
      0: 'input_back'
    }
  },

'reboot_bot': {
    'text': 'Do you really want to reboot the bot? This can solve issues if the bot got stuck but all users need to restart their query after the bot rebooted.',
    'type': 'select',
    'answers': ['Yes', 'Cancel'],
    'logic':{
      0: 'confirm_reboot',
      1: 'start'
    } 
  },
     'confirm_reboot': {
    'text': "Okay, click /reboot to restart the bot. Wait for some seconds and type /start afterwards.",
    'type': 'input',
    'value': '',
    'var': '',
    'success': '',
    'answers': ['<< Back'],
        'logic':{
      0: 'start'
    }
}
}