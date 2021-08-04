# Parse dates experiments
# @source https://ru.stackoverflow.com/questions/419321/%D0%9F%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B4%D0%B0%D1%82%D1%8B-%D0%BC%D0%B5%D0%B6%D0%B4%D1%83-%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8-%D0%BF%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%D0%BC%D0%B8
#!/usr/bin/env python3
from datetime import datetime
import icu # PyICU , setup: pip install icu

date_strings = ['Март 1, 2010', 'Сен. 1, 2010', '2015-Апрель-26']
print(date_strings)

df = icu.SimpleDateFormat('', icu.Locale('ru'))
output_df = icu.SimpleDateFormat('yyyy-MM-dd')

output_date_strings = []
for date_str in date_strings:
    date_str = date_str.replace('Сен.', 'Сент.') # fix the abbr.
    for pattern in 'LLLL d, yyyy', 'yyyy-LLLL-dd':
        df.applyPattern(pattern)
        try:
            output_date_strings.append(output_df.format(df.parse(date_str)))
        except icu.ICUError:
            pass
        else:
            break
    else:
        print('failed to parse %r' % date_str)

print(output_date_strings)