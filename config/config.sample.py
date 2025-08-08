# -*- coding: utf-8 -*-

import os

# Пути к файлам
SQLITE3_DB_PATH = '../db/logger.db'
LOG_FILENAME = '../db/logger.log'
IMPORT_FILE = '../import/TimePlannerExport.html'

# Email настройки
DEBUG_SEND_TO = [
    'test@mail.ru',
]
MAIL_FROM = "TimeLogger <noreply@timelogger.com>"
USER_ID = "test"

# Google Calendar API настройки
GOOGLE_CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar']
GOOGLE_CALENDAR_ID = 'test@test.com'
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'timeplanner.sample.json')