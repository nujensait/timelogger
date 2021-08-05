# COMMON FUNCTIONS

import locale       # for russian locale usage
import re           # regexp
from datetime import datetime

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

    dat = ""
    for date_fmt in date_formats:
        try:
            date_time = datetime.strptime(date_str, date_fmt)
            dt = "%s %s" % (date_time.date() , date_time.time())
        except ValueError:
            pass
        else:
            break
    else:
        dt = ""
        # print('failed to parse %r' % date_str)
    return str(dt)
