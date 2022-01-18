# Parse dates experiments
# @source https://ru.stackoverflow.com/questions/419321/%D0%9F%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B4%D0%B0%D1%82%D1%8B-%D0%BC%D0%B5%D0%B6%D0%B4%D1%83-%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8-%D0%BF%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%D0%BC%D0%B8
# mapping variants: https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
#!/usr/bin/env python3

# read libs in parent dir
import sys
sys.path.insert(0, '..')

from common.functions import convert_tp_date, set_locale
import datetime
import locale

date_strings = [
    '2022-01-18',                   # OK : 2022-01-18 00:00:00
    '2022-01-18 12:38:05',          # OK : 2022-01-18 12:40:00
    '18 янв. 2022 г.',              # OK : 2022-01-18 00:00:00
    '18 January 2022',              # OK : 2022-01-18 00:00:00
    '18 Января 2022',               # OK : 2022-01-18 00:00:00
    'Март 1, 2010',                 # OK : 2010-03-01 00:00:00
    'Сен. 1, 2010',                 # OK : 2010-09-01 00:00:00
    '2015-Апрель-26',               # OK: 2015-04-26 00:00:00
    '4 авг. 2021 г.',               # OK: 2021-08-04 00:00:00
    # add times
    '4 авг. 2021 г. 11:50',         # OK : 2021-08-04 11:50:00
    '3 сен. 2023 г. 11: 32',        # OK : 2023-09-03 11:30:00
    '3 сен. 2023 г. 11: 70'         # wrong date
]

########################################################################################################################
# Test function

set_locale()

dt = datetime.datetime.now();
#today = dt.strftime("%Y-%m-%dT%H:%M:%S+03:00");
today = dt.strftime("%Y %B %d %H:%M:%S");

print("Today: " + today)

########################################################################################################################

print(date_strings)

# convert dates
for date_str in date_strings:
    dt = convert_tp_date(date_str)
    if(dt != ""):
        print(dt)
    else:
        print("[!] Wrong date: " + date_str)