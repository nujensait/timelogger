# COMMON FUNCTIONS

import locale       # for russian locale usage
import re           # regexp
import datetime

def convert_tp_time(time_str):
    replaced = re.sub('[^\d\:]', '', time_str)
    return replaced

# Convert date: rus (TimePlanner) ==> eng (python)
def convert_tp_date(date_str):

    #locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')        # linux, the ru locale is installed
    locale.setlocale(locale.LC_TIME, locale="Russian")      # windows, works

    # @hint date-time formats: https://pythononline.ru/osnovy/strptime-python
    # variative dates masks
    date_formats = '%B %d, %Y', \
                   '%b %d, %Y', \
                   '%Y-%B-%d', \
                   '%d %B %Y', \
                   '%d %B %Y г.', \
                   '%d %B %Y г. %H:%M', \
                   '%d %B %Y г. %H: %M'

    # rename months:
    date_str = date_str.lower()
    months_mapping = ("янв.",   "январь"), \
                     ("февр.",  "февраль"), \
                     ("мар.",   "март"), \
                     ("апр.",   "апрель"), \
                     ("май.",   "май"), \
                     ("июн.",   "июнь"), \
                     ("июл.",   "июль"), \
                     ("авг.",   "август"), \
                     ("сен.",   "сентябрь"), \
                     ("окт.",   "октябрь"), \
                     ("ноя.",   "ноябрь"), \
                     ("дек.",   "декабрь")

    for r in months_mapping:
        date_str = date_str.replace(*r)

    for date_fmt in date_formats:
        try:
            date_time = datetime.datetime.strptime(date_str, date_fmt)
            date_time = roundTime(date_time, 10)        # round to closest :10 min
            dt = "%s %s" % (date_time.date() , date_time.time())
        except ValueError:
            pass
        else:
            break
    else:
        dt = ""
        # print('failed to parse %r' % date_str)
    return str(dt)

"""Round a datetime object to a multiple of a timedelta
@source https://visdap.blogspot.com/2019/02/how-to-round-minute-of-datetime-object.html
dt : datetime.datetime object, default now.
dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
Author: Thierry Husson 2012 - Use it as you want but don't blame me.
        Stijn Nevens 2014 - Changed to use only datetime objects as variables
"""
def roundTime(dt = None, roundTo = 10):
    dateDelta = datetime.timedelta(minutes=roundTo)
    roundTo = dateDelta.total_seconds()
    if dt == None : dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)