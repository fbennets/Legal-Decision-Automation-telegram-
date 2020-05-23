
user_menu_data = {
  'start' : {
    'text': 'What do you want to do?',
    'type': 'select',
    'answers': ['Show available queries', 'Enter access code', 'Start Demo', 'Know More', 'Change Language'],
    'logic':{
      0: 'show_queries',
      1: 'enter_access_code',
      2: 'start_demo',
      3: 'know_more',
      4: 'change_language'
    } 
  },
  'show_queries': {
    'text': 'These queries are available',
    'type': 'select',
    'answers': ['<< Back'],
    'logic':{
      0: 'query3',
      1: 'query2',
      2: 'query1',
      3: 'start',
    } 
  },

   'know_more': {
    'text': "",
    'type': 'show_info',
    'answers': ['<< Back'],
    'logic':{
      0: 'back'
    }
  },
     'enter_access_code': {
    'text': "",
    'type': 'input',
    'answers': ['<< Back'],
    'logic':{
      0: 'back'
    }
  },

     'change_language': {
    'text': "Select one of the languages:",
    'type': 'show_info',
    'answers': ['<< Back'],
    'logic':{
      0: 'back'
    }
  },
}