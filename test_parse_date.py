# Parse dates experiments
# @source https://ru.stackoverflow.com/questions/419321/%D0%9F%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B4%D0%B0%D1%82%D1%8B-%D0%BC%D0%B5%D0%B6%D0%B4%D1%83-%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8-%D0%BF%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%D0%BC%D0%B8
# mapping variants: https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
#!/usr/bin/env python3

from common.functions import convert_tp_date

date_strings = ['Март 1, 2010',
                'Сен. 1, 2010',
                '2015-Апрель-26',
                '12 июнь 2021',
                '13 июнь 2021 г.',
                '14 июн. 2021 г.',
                '3 июл. 2021 г.',
                '4 авг. 2021 г.',
                # add times
                '4 авг. 2021 г. 11:50',
                '3 сен. 2023 г. 11: 30',
                '3 сен. 2023 г. 11: 70'     # wrong date
                ]

########################################################################################################################
# Test function

print(date_strings)

for date_str in date_strings:
    dt = convert_tp_date(date_str)
    print(dt)