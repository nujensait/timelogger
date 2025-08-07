# Makefile для TimeLogger
# Автор: Иконников Михаил

.PHONY: help setup run

# Команда по умолчанию - выводит справку
help:
	@echo "Доступные команды:"
	@echo "  make setup  - Установка всех необходимых зависимостей"
	@echo "  make run    - Запуск локального веб-сервера"
	@echo "  make help   - Показать справку"

# Установка всех необходимых зависимостей
setup:
	pip install --upgrade pip
	python -m pip install --upgrade pip
	pip install --upgrade google-api-python-client
	pip install bs4
	pip install wheel
	pip install lxml

# Запуск локального веб-сервера
run:
	@echo "Запуск локального HTTP веб-сервера на порту 8000..."
	@echo "Откройте страницу загрузки файлов: http://localhost:8000/upload.py"
	@echo "ИЛИ (если вы используете WAMP/OSPanel): http://timelogger/upload.py"
	python -m http.server
