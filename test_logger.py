#!/usr/bin/python3
# Export parsed html file date to Google calendar

from __future__ import print_function
import sys
import sqlite3

# read libs in parent dir
#sys.path.insert(0, '')

from logger import TimeLogger
import config

print("[ START ]")

logger = TimeLogger()

conn = sqlite3.connect(config.sqlite3_db_path)
cursor = conn.cursor()

if '--action=create_tables' in sys.argv:
    logger.create_logger_tables(conn)
    exit(1)

if '--action=drop_tables' in sys.argv:
    logger.drop_logger_tables(conn)
    exit(1)

# parse events from file
events = logger.parse_events_file(conn, config.IMPORT_FILE)

# parse events
events_dict = logger.create_events_dict(events)

# save events to calendar
logger.create_calendar_events(events_dict)

# finish
print("[ FINISH ]")
conn.close()
