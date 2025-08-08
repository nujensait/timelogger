# Test time rounding
# @source https://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object/10854034#10854034

import pytest
from datetime import datetime
import sys
import os

# Для обеспечения доступа к модулям из родительской директории
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.functions import roundTime

def test_round_time_5min():
    """Тест округления времени с интервалом 5 минут"""
    # Тест округления вверх
    dt1 = datetime.fromisoformat("2021-06-30 09:19:03")
    expected1 = datetime.fromisoformat("2021-06-30 09:20:00")
    result1 = roundTime(dt1, roundTo=5)
    assert result1 == expected1, f"Expected {expected1}, but got {result1}"
    
    # Тест округления вниз
    dt2 = datetime.fromisoformat("2021-06-30 09:12:03")
    expected2 = datetime.fromisoformat("2021-06-30 09:10:00")
    result2 = roundTime(dt2, roundTo=5)
    assert result2 == expected2, f"Expected {expected2}, but got {result2}"

def test_round_time_default():
    """Тест округления времени с дефолтным интервалом (60 минут)"""
    dt = datetime.fromisoformat("2021-06-30 09:08:00")
    expected = datetime.fromisoformat("2021-06-30 09:00:00")
    result = roundTime(dt)
    assert result == expected, f"Expected {expected}, but got {result}"

def test_round_time_30min():
    """Тест округления времени с интервалом 30 минут"""
    dt = datetime(2012, 12, 31, 23, 44, 49)
    expected = datetime(2012, 12, 31, 23, 30, 0)
    result = roundTime(dt, 30)
    assert result == expected, f"Expected {expected}, but got {result}"
