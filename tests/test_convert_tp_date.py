# Parse dates experiments
# @source https://ru.stackoverflow.com/questions/419321/%D0%9F%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B4%D0%B0%D1%82%D1%8B-%D0%BC%D0%B5%D0%B6%D0%B4%D1%83-%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%BE%D0%B2%D1%8B%D0%BC%D0%B8-%D0%BF%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%D0%BC%D0%B8
# mapping variants: https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string

import pytest
import sys
import os
import datetime

# Для доступа к модулям из родительской директории
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.functions import convert_tp_date, set_locale

@pytest.fixture(scope="module", autouse=True)
def setup_locale():
    """Установка локали перед всеми тестами"""
    set_locale()

def test_simple_date_formats():
    """Тесты простых форматов даты"""
    # ISO формат без времени
    dt1 = convert_tp_date('2022-01-18')
    assert dt1 == '2022-01-18 00:00:00', f"Expected '2022-01-18 00:00:00', got {dt1}"
    
    # ISO формат с временем
    dt2 = convert_tp_date('2022-01-18 12:38:05')
    assert dt2 == '2022-01-18 12:40:00', f"Expected '2022-01-18 12:40:00', got {dt2}"

def test_russian_date_formats():
    """Тесты русских форматов даты"""
    # Русский формат с сокращениями
    dt1 = convert_tp_date('18 янв. 2022 г.')
    assert dt1 == '2022-01-18 00:00:00', f"Expected '2022-01-18 00:00:00', got {dt1}"
    
    # Русский формат с полным названием месяца
    dt2 = convert_tp_date('18 Января 2022')
    assert dt2 == '2022-01-18 00:00:00', f"Expected '2022-01-18 00:00:00', got {dt2}"

def test_english_date_formats():
    """Тесты английских форматов даты"""
    # Английский формат
    dt = convert_tp_date('18 January 2022')
    assert dt == '2022-01-18 00:00:00', f"Expected '2022-01-18 00:00:00', got {dt}"

def test_unusual_date_formats():
    """Тесты необычных форматов даты"""
    # Формат 'Месяц день, год'
    dt1 = convert_tp_date('Март 1, 2010')
    assert dt1 == '2010-03-01 00:00:00', f"Expected '2010-03-01 00:00:00', got {dt1}"
    
    # Формат с сокращённым названием месяца
    dt2 = convert_tp_date('Сен. 1, 2010')
    assert dt2 == '2010-09-01 00:00:00', f"Expected '2010-09-01 00:00:00', got {dt2}"
    
    # Формат 'год-месяц-день'
    dt3 = convert_tp_date('2015-Апрель-26')
    assert dt3 == '2015-04-26 00:00:00', f"Expected '2015-04-26 00:00:00', got {dt3}"

def test_date_with_time():
    """Тесты дат со временем"""
    # Формат даты с временем
    dt1 = convert_tp_date('4 авг. 2021 г. 11:50')
    assert dt1 == '2021-08-04 11:50:00', f"Expected '2021-08-04 11:50:00', got {dt1}"
    
    # Формат даты с некорректным форматом времени
    dt2 = convert_tp_date('3 сен. 2023 г. 11: 32')
    assert dt2 == '2023-09-03 11:30:00', f"Expected '2023-09-03 11:30:00', got {dt2}"

def test_invalid_date():
    """Тест некорректной даты"""
    # Дата с неправильным временем
    dt = convert_tp_date('3 сен. 2023 г. 11: 70')
    assert dt == "", f"Expected empty string for invalid date, got {dt}"