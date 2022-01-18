#!/usr/bin/python3
# Export parsed html file date to Google calendar

# read libs in parent dir
import sys
sys.path.insert(0, '..')

from __future__ import print_function
import sys
from logger import TimeLogger
import config
import sqlite3

print("[ START ]")

logger = TimeLogger()

conn = sqlite3.connect(config.sqlite3_db_path)
cursor = conn.cursor()

if '--action=create_table' in sys.argv:
    logger.create_logger_table(conn)
    exit(1)

# parse events
events = logger.create_events_dict(conn, config.IMPORT_FILE)

# save events to calendar
logger.create_calendar_events(events)

# finish
print("[ FINISH ]")
conn.close()
