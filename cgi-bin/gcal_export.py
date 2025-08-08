#!/usr/bin/env python3
# Sync: Python <===> Google calendar
# @source https://habr.com/ru/post/525680/

from __future__ import print_function
import os
import sys
import datetime
import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Импортируем настройки из конфига
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config

class GcalExport(object):
    """
    Класс для работы с Google Calendar API.
    Позволяет создавать события и получать список событий из календаря.
    """
    def __init__(self):
        """
        Инициализация объекта GoogleCalendar.
        Создает подключение к Google Calendar API с использованием сервисного аккаунта.
        """
        try:
            credentials = service_account.Credentials.from_service_account_file(
                config.SERVICE_ACCOUNT_FILE, 
                scopes=config.GOOGLE_CALENDAR_SCOPES
            )
            self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
        except FileNotFoundError:
            # Для тестов без реальных учетных данных
            self.service = None

    # создание словаря с информацией о событии
    def create_event_dict(self):
        """
        Создает словарь с данными события для календаря.
        
        Returns:
            dict: Словарь с информацией о событии.
        """
        event = {
            'summary': 'test event',
            'description': 'some info',
            'start': {
                'dateTime': '2020-08-03T03:00:00+03:00',
            },
            'end': {
                'dateTime': '2020-08-03T05:30:00+03:00',
            }
        }
        return event

    # создание события в календаре
    def create_event(self, event):
        """
        Создает событие в календаре.
        
        Args:
            event (dict): Словарь с информацией о событии.
            
        Returns:
            str: ID созданного события или None в случае ошибки.
        """
        if self.service is None:
            return "mock-event-id"
        e = self.service.events().insert(calendarId=config.GOOGLE_CALENDAR_ID, body=event).execute()
        return e.get('id')

    # вывод списка из десяти предстоящих событий
    def get_events_list(self):
        """
        Получает список предстоящих событий из календаря.
        
        Returns:
            list: Список событий или пустой список, если события не найдены.
        """
        if self.service is None:
            return []
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(
            calendarId=config.GOOGLE_CALENDAR_ID,
            timeMin=now,
            maxResults=10, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])
