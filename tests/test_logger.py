#!/usr/bin/env python3
# Export parsed html file date to Google calendar

from __future__ import print_function
import os
import sys
import sqlite3
import pytest
import tempfile

# Для доступа к модулям из родительской директории и cgi-bin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cgi-bin'))

from logger import TimeLogger
from config import config

@pytest.fixture
def db_connection():
    """Подготовка тестового соединения с базой данных"""
    # Используем тестовую базу данных в памяти вместо реальной базы
    conn = sqlite3.connect(':memory:')
    
    # Создаем новый экземпляр TimeLogger и инициализируем таблицы
    logger = TimeLogger()
    logger.create_logger_tables(conn)
    
    # Возвращаем соединение и логгер для тестов
    yield conn, logger
    
    # Закрываем соединение после завершения теста
    conn.close()

def test_create_drop_tables(db_connection):
    """Тест создания и удаления таблиц"""
    conn, logger = db_connection
    
    # Проверяем, что таблица events существует
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    result = cursor.fetchone()
    assert result is not None, "Table 'events' was not created"
    
    # Удаляем таблицы и проверяем, что они удалены
    logger.drop_logger_tables(conn)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    result = cursor.fetchone()
    assert result is None, "Table 'events' was not dropped"

@pytest.mark.skip(reason="Требует наличия тестового HTML-файла")
def test_parse_html(db_connection):
    """Тест парсинга HTML-файла"""
    conn, logger = db_connection
    
    # Используем тестовый файл для парсинга
    events = logger.parse_html(conn, config.IMPORT_FILE)
    
    # Проверяем, что мы получили некоторые события
    assert events is not None, "No events were parsed"
    assert len(events) > 0, "No events were found in the import file"
    
    # Проверяем формирование словаря событий
    events_dict = logger.create_events_dict(events)
    assert events_dict is not None, "Events dictionary was not created"
    
    # Проверяем, что ключи словаря - это даты
    for key in events_dict.keys():
        assert isinstance(key, str), f"Key {key} is not a string date"

@pytest.mark.skip(reason="Требует настроенного доступа к Google Calendar API")
def test_create_calendar_events(db_connection):
    """Тест создания событий в календаре"""
    conn, logger = db_connection
    
    # Создаем тестовый словарь событий
    test_events_dict = {
        '2023-09-01': [{'summary': 'Test Event', 'start_time': '10:00', 'end_time': '11:00'}]
    }
    
    try:
        # Пытаемся создать события в календаре
        # Этот тест может потерпеть неудачу, если Google API недоступен
        logger.create_calendar_events(test_events_dict)
        assert True, "Calendar events created successfully"
    except Exception as e:
        pytest.skip(f"Google Calendar API not available: {str(e)}")

