# Export parsed html file date to Google calendar

from __future__ import print_function
import datetime
import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
import re
from bs4 import BeautifulSoup
from common.functions import convert_tp_date, convert_tp_time, roundTime

SCOPES = ['https://www.googleapis.com/auth/calendar']

calendarId = 'mishaikon@gmail.com'; #'lp285psodk309lilp73d9irek8@group.calendar.google.com'
SERVICE_ACCOUNT_FILE = 'timeplanner-321909-44d96c49fe5d.json'

########################################################################################################################

class TimeLogger(object):

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    # создание словаря с информацией о событии
    def create_events_dict_deprecated(self):
        events = [{
            'summary': 'test event',
            'description': 'some info',
            'start': {
                'dateTime': '2020-08-03T03:00:00+03:00',
            },
            'end': {
                'dateTime': '2020-08-03T05:30:00+03:00',
            }
        }]
        return events

    # Read events from html, store it to dict
    def create_events_dict(self, file):
        events = self.parse_html(file)
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
        e = self.service.events().insert(calendarId=calendarId,
                                         body=event).execute()
        print('Event created: %s' % (e.get('id')))

    # Parse html file: exctract actions data
    def parse_html(self, file_name):

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
                        # round times
                        #date_start = roundTime(date_start, 10)
                        #date_end   = roundTime(date_end, 10)
                        # action name can be empty...
                        name       = str(cells[2].find(text=True) or '')
                        # add category name to action name:
                        name       = "%s / %s" % (cat , name) if name != "" else cat
                        #print("{0}\t{1}\t{2}".format(date_start, date_end, name))
                        events.append({
                            "date_start": date_start,
                            "date_end": date_end,
                            "name": name
                        })
            return events


########################################################################################################################

logger = TimeLogger()

# parse events
events = logger.create_events_dict("import/time_planner_logged_activities_2021-06-30.html")

# save events to calendar
logger.create_events(events)
