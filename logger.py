#!C:\Users\misha\AppData\Local\Programs\Python\Python310\python.exe
# Export parsed html file date to Google calendar
# Unix: !/usr/bin/python3

from __future__ import print_function
from datetime import datetime
import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

import config
from common.functions import convert_tp_date, convert_tp_time
from pprint import pprint
import sqlite3

########################################################################################################################

class TimeLogger(object):

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(config.SERVICE_ACCOUNT_FILE,
                                                                            scopes=config.SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    # Store it to dict (suitable for export into Goggle calendar)
    def create_events_dict(self, events):
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
    @staticmethod
    def make_calendar_date(dt):
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%dT%H:%M:%S+03:00")

    # create multiple events
    def create_calendar_events(self, events):
        for event in events:
            self.create_event(event)

    # создание события в календаре
    def create_event(self, event):
        e = self.service.events().insert(calendarId=config.CALENDAR_ID, body=event).execute()
        print("\nCalendar event created: %s <br />\n" % (e.get('id')))

    # print events table
    def print_events(self, events):
        print("<h3>Импортируемые данные:</h3>")
        print("<table cellpadding=5 cellspacing=0 border=1>")
        print("<tr><th>Дата начала</th><th>Дата завершения</th><th>Событие</th></tr>")
        # output parsed data
        for event in events:
            print("<tr>")
            print("<td>" + event.get('date_start') + "</td>\n")
            print("<td>" + event.get('date_end') + "</td>\n")
            print("<td>" + event.get('name') + "</td>\n")
            print("</tr>")
        print("</table>")

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
                        try:
                            time = cells[0].find(text=True)
                            date = cells[1].find(text=True)
                            # convert date to proper format, ex: 3 авг. 2021 г. => '2020-08-03T00:00:00+03:00'
                            times = time.split('- ')
                            time1 = convert_tp_time(times[0])
                            time2 = convert_tp_time(times[1])
                            # make classic dateTimes, like: '2021-06-30 17:42:00'
                            date_start = convert_tp_date("%s %s" % (date, time1))
                            date_end = convert_tp_date("%s %s" % (date, time2))
                        except Exception as e:
                            # print("Error: wrong event date/time: " + time);
                            continue

                        # action name can be empty...
                        name = str(cells[2].find(text=True) or '')
                        # add category name to action name:
                        name = "%s / %s" % (cat, name) if name != "" else cat
                        # print("{0}\t{1}\t{2}".format(date_start, date_end, name))

                        # create event if not exists
                        exist = self.event_exist(conn, date_start, date_end)
                        if not exist:
                            events.append({
                                "date_start": date_start,
                                "date_end": date_end,
                                "name": name
                            })
                            self.save_event(conn, date_start, date_end, name)

            return events

    # create logger
    def create_logger_tables(self, conn):
        cursor = conn.cursor()
        print("[ CREATE TABLE 'events' ... ]\n")
        cursor.execute("""CREATE TABLE events
                          (user_id     		    text,
                           category             text, 
                           name    		        text,
                           date_start           datetime,
                           date_end             datetime,
                           time_start           timestamp, 
                           time_end             timestamp,
                           time_import          timestamp
                           )
                        """)
        conn.commit()
        print("[ CREATE DONE ]\n")

    # create logger
    def drop_logger_tables(self, conn):
        cursor = conn.cursor()
        print("[ DROP TABLE 'events' ... ]\n")
        cursor.execute("""DROP TABLE events""")
        conn.commit()
        print("[ DROP DONE ]\n")

    # check that event exists
    def event_exist(self, conn, date_start, date_end):
        cursor = conn.cursor()
        query = """
            SELECT count(*) as exist
            FROM events 
            WHERE date_start = '%s'             
              AND date_end   = '%s'
            """ % (date_start, date_end)
        cursor.execute(query)
        records = cursor.fetchall()
        return 1 if records[0][0] > 0 else 0

    # save event to DB
    def save_event(self, conn, date_start, date_end, name):
        cursor      = conn.cursor()  # db connection
        time_start  = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S").timestamp()
        time_end    = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S").timestamp()
        time_import = datetime.now().timestamp()
        # save to DB
        sql = "INSERT INTO events " \
              "(user_id, name, date_start, date_end, time_start, time_end, time_import) " \
              "VALUES (?, ?, ?, ?, ?, ?, ?)";
        result = cursor.execute(sql, [config.USER_ID, name, date_start, date_end, time_start, time_end, time_import])

        # Save (commit) the changes
        conn.commit()

        #print(result)
        #print(sql)
        #print("<br >")
        return result

########################################################################################################################
