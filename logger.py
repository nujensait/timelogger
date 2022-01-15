# Export parsed html file date to Google calendar

from __future__ import print_function
import datetime
import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

import config
from common.functions import convert_tp_date, convert_tp_time, roundTime
from pprint import pprint
from clickhouse_driver.client import Client
import sqlite3

########################################################################################################################

class TimeLogger(object):

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(config.SERVICE_ACCOUNT_FILE, scopes=config.SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    # Read events from html, store it to dict
    def create_events_dict(self, conn, file):
        events = self.parse_html(conn, file)
        # make events dict
        dict = []
        for event in events:
            dict.append({
                'summary': event.get('name'),
                'description': '',
                'start': {
                    'dateTime': self.make_calendar_date(event.get('date_start')),
                },
                'end': {
                    'dateTime': self.make_calendar_date(event.get('date_end')),
                }
            })
        return dict

    # convert python date to google calendar date
    # '2020-08-03 03:00:00' ==> '2020-08-03T03:00:00+03:00'
    def make_calendar_date(self, dt):
        dt = datetime.datetime.fromisoformat(dt)
        return dt.strftime("%Y-%m-%dT%H:%M:%S+03:00")

    # create multiple events
    def create_events(self, events):
        for event in events:
            self.create_event(event)

    # создание события в календаре
    def create_event(self, event):
        e = self.service.events().insert(calendarId=config.CALENDAR_ID, body=event).execute()
        print('Event created: %s' % (e.get('id')))

    # Parse html file: exctract actions data
    def parse_html(self, conn, file_name):

        with open(file_name, encoding="utf8") as f:

            # read file
            contents = f.read()

            # load as DOM
            soup = BeautifulSoup(contents, 'lxml')

            # Calendar events & it's categories
            events = []
            cats = []
            for cat in soup.find_all("b"):
                cats.append(cat.text)

            tables = soup.findAll("table", {"cellpadding": "10"})
            for table in tables:
                cat = cats.pop(0)
                for row in table.findAll("tr"):
                    cells = row.findAll("td")
                    if len(cells) == 3:
                        time       = cells[0].find(text=True)
                        date       = cells[1].find(text=True)
                        # convert date to proper format, ex: 3 авг. 2021 г. => '2020-08-03T00:00:00+03:00'
                        times      = time.split('- ')
                        time1      = convert_tp_time(times[0])
                        time2      = convert_tp_time(times[1])
                        # make classic dateTimes, like: '2021-06-30 17:42:00'
                        date_start = convert_tp_date("%s %s" % (date, time1))
                        date_end   = convert_tp_date("%s %s" % (date, time2))
                        # action name can be empty...
                        name       = str(cells[2].find(text=True) or '')
                        # add category name to action name:
                        name       = "%s / %s" % (cat , name) if name != "" else cat
                        #print("{0}\t{1}\t{2}".format(date_start, date_end, name))
                        # create event if not exists
                        exist      = self.event_exist(conn, date_start, date_end)
                        if(not exist):
                            events.append({
                                "date_start": date_start,
                                "date_end": date_end,
                                "name": name
                            })
                            self.save_event(conn, date_start, date_end, name)
            return events

    # create logger
    def create_logger_table(self, conn):
        cursor = conn.cursor()
        print("[ CREATE TABLE 'events' ... ]\n")
        cursor.execute("""CREATE TABLE events
                          (user_id     		    text, 
                           name    		        text,
                           date_start           text,
                           date_end             text,
                           time_start           timestamp, 
                           time_end             timestamp,
                           time_import          timestamp
                           )
                        """)
        conn.commit()
        print("[ CREATE DONE ]\n")

    # check that event exists
    def event_exist(self, conn, date_start, date_end):
        cursor = conn.cursor()
        clickhouse_query = """
            SELECT count(*) as exist
            FROM events 
            WHERE date_start = '%s'             
              AND date_end   = '%s'
            """ % ( date_start, date_end)
        result = cursor.execute(clickhouse_query)
        records = cursor.fetchall()
        return (1 if records[0][0] > 0 else 0)

    # save event to DB
    def save_event(self, conn, date_start, date_end, name):
        cursor = conn.cursor()
        time_start  = datetime.datetime.fromisoformat(date_start).timestamp()
        time_end    = datetime.datetime.fromisoformat(date_end).timestamp()
        time_import = datetime.datetime.now().timestamp()
        cursor.execute("INSERT INTO events VALUES ('%s', '%s', '%s', '%s', %d, %d, %d)" % (config.USER_ID, name, date_start, date_end, time_start, time_end, time_import))


########################################################################################################################

