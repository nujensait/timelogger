# COMMON FUNCTIONS

import locale       # for russian locale usage
import re           # regexp
import datetime

def convert_tp_time(time_str):
    replaced = re.sub('[^\d\:]', '', time_str)
    return replaced

def set_locale():
    #set_ru_locale()
    set_en_locale()

def set_en_locale():
    try:
        locale.setlocale(locale.LC_TIME, 'en')  # Use ENG locale otherwise
    except Exception as e:
        print('An error occurred on locale setting: {0}'.format(e))
        exit();

def set_ru_locale():
    try:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')             # linux, the ru locale is installed
    except Exception:
        try:
            locale.setlocale(locale.LC_TIME, locale="Russian")      # windows, works
        except Exception as e:
            print('An error occurred on locale setting: {0}'.format(e))
            exit();

# Convert date: rus (TimePlanner) ==> eng (python)
def convert_tp_date(date_str):

    # try to set locale
    set_locale()

    # @hint date-time formats: https://pythononline.ru/osnovy/strptime-python
    # variative dates masks
    date_formats = '%Y-%m-%d %H:%M:%S', \
                   '%Y-%m-%d', \
                   '%B %d, %Y', \
                   '%b %d, %Y', \
                   '%Y-%B-%d', \
                   '%d %B %Y', \
                   '%d %B %Y г.', \
                   '%d %B %Y г. %H:%M', \
                   '%d %B %Y г. %H: %M'

    # convert to lowercase first
    date_str = date_str.lower()

    ru_months_mapping = ("янв.",   "Январь"), \
                     ("февр.",  "Февраль"), \
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

    months_mapping = ("янв.",   "January"), \
                     ("февр.",  "Febrary"), \
                     ("мар.",   "March"), \
                     ("апр.",   "April"), \
                     ("май.",   "May"), \
                     ("июн.",   "June"), \
                     ("июл.",   "July"), \
                     ("авг.",   "August"), \
                     ("сен.",   "September"), \
                     ("окт.",   "October"), \
                     ("ноя.",   "Noovember"), \
                     ("дек.",   "December"), \
                     ("январь",   "January"), \
                     ("февраль",  "Febrary"), \
                     ("март",   "March"), \
                     ("апрель",   "April"), \
                     ("май",   "May"), \
                     ("июнь",   "June"), \
                     ("июль",   "July"), \
                     ("август",   "August"), \
                     ("сентябрь",   "September"), \
                     ("октябрь",   "October"), \
                     ("ноябрь",   "Noovember"), \
                     ("декабрь",   "December"), \
                     ("января", "January"), \
                     ("февраля", "Febrary"), \
                     ("марта", "March"), \
                     ("апреля", "April"), \
                     ("мая", "May"), \
                     ("июня", "June"), \
                     ("июля", "July"), \
                     ("августа", "August"), \
                     ("сентября", "September"), \
                     ("октября", "October"), \
                     ("ноября", "Noovember"), \
                     ("декабря", "December")

    for r in months_mapping:
        date_str = date_str.replace(*r)

    for date_fmt in date_formats:
        try:
            date_time = datetime.datetime.strptime(date_str, date_fmt)
            date_time = roundTime(date_time, 10)        # round to closest :10 min
            dt = "%s %s" % (date_time.date() , date_time.time())
            #print(date_str + "====>" + str(dt))
        except Exception as e:
            #print(e)        # on debug mode
            pass
        else:
            break
    else:
        dt = ""
        #print('failed to parse %r' % date_str)
    return str(dt)

""" Round a datetime object to a multiple of a timedelta
dt : datetime.datetime object, default now.
dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
@source https://visdap.blogspot.com/2019/02/how-to-round-minute-of-datetime-object.html
"""
def roundTime(dt = None, roundTo = 10):
    dateDelta = datetime.timedelta(minutes=roundTo)
    roundTo = dateDelta.total_seconds()
    if dt == None : dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)