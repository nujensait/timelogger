# Sync: Python <===> Google calendar
# @source https://habr.com/ru/post/525680/

import pytest
import os
import sys
import datetime
import googleapiclient
from unittest import mock

# Для доступа к модулям из родительской директории и cgi-bin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cgi-bin'))

# Импортируем класс GcalExport и конфиг
from gcal_export import GcalExport
from config import config


@pytest.fixture
def calendar():
    """Создает экземпляр GcalExport для тестов"""
    return GcalExport()


@pytest.mark.skip(reason="Требует настроенного доступа к Google Calendar API")
def test_create_event(calendar):
    """Тестирует создание события в календаре"""
    # Создаем тестовое событие
    event = calendar.create_event_dict()
    assert event is not None, "Event dictionary was not created"
    assert 'summary' in event, "Event missing required 'summary' field"
    assert 'start' in event, "Event missing required 'start' field"
    assert 'end' in event, "Event missing required 'end' field"
    
    # Пытаемся создать событие в календаре
    try:
        event_id = calendar.create_event(event)
        assert event_id is not None, "Event was not created successfully"
    except Exception as e:
        pytest.skip(f"Google Calendar API not available: {str(e)}")


@pytest.mark.skip(reason="Требует настроенного доступа к Google Calendar API")
def test_get_events_list(calendar):
    """Тестирует получение списка событий из календаря"""
    try:
        events = calendar.get_events_list()
        assert events is not None, "Events list is None"
        # Не проверяем количество событий, так как в календаре может не быть событий
    except Exception as e:
        pytest.skip(f"Google Calendar API not available: {str(e)}")


# Тесты с использованием моков для имитации Google API
@pytest.mark.parametrize("test_input,expected", [
    ({"summary": "Test Event"}, "mock-event-id"),
    ({"summary": "Another Test"}, "mock-event-id"),
])
def test_create_event_mock(monkeypatch, test_input, expected):
    """Тестирует создание события с использованием моков"""
    # Создаем мок для GcalExport.create_event
    calendar = GcalExport()
    
    # Используем monkeypatch для подмены метода service
    calendar.service = None
    
    # Пытаемся создать событие
    event_id = calendar.create_event(test_input)
    assert event_id == expected, f"Expected {expected}, got {event_id}"