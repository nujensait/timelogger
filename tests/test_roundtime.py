# Test time rounding
# @source https://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object/10854034#10854034
# !/usr/bin/env python3

# read libs in parent dir
import sys

sys.path.insert(0, '..')

from datetime import datetime
from common.functions import roundTime

dt = datetime.fromisoformat("2021-06-30 09:19:03")
print(dt)
print(roundTime(dt, roundTo=5))
print()
# 2021-06-30 09:20:00

dt = datetime.fromisoformat("2021-06-30 09:12:03")
print(dt)
print(roundTime(dt, roundTo=5))
print()
# 2021-06-30 09:10:00

dt = datetime.fromisoformat("2021-06-30 09:08:00")
print(dt)
print(roundTime(dt))
print()
# 2021-06-30 09:00:00

print(roundTime(datetime(2012, 12, 31, 23, 44, 49), 30))
# 2012-12-31 23:30:00
