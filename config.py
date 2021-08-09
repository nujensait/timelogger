# -*- coding: utf-8 -*-

# logging
LOG_FILENAME            = 'logger.log'

# sqlite
sqlite3_db_path         = 'logger.db'

# email notifications settings
debug_send_to           = [
    'mishakon@gmail.com',
]
mail_from               = "TimeLogger <noreply@timelogger.com>"

# Calendar settings
# get/create settings from here: https://habr.com/ru/post/525680/
SERVICE_ACCOUNT_FILE    = 'timeplanner-321909-44d96c49fe5d.json'
CALENDAR_ID             = 'mishaikon@gmail.com'
SCOPES                  = ['https://www.googleapis.com/auth/calendar']
IMPORT_FILE             = "import/time_planner.html"
USER_ID                 = "mishaikon"