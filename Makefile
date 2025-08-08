# Makefile для TimeLogger
# запускать в среде linux или wsl (в windows)
# Пример запуска:
# make setup

.PHONY: help setup run setup-cgi test

# Команда по умолчанию - выводит справку
help:
	@echo "Доступные команды:"
	@echo "  make setup  - Установка всех необходимых зависимостей"
	@echo "  make run    - Запуск локального веб-сервера"
	@echo "  make help   - Показать справку"

# Установка всех необходимых зависимостей
setup:
	pip install --upgrade pip
	sudo python3 -m pip install --upgrade pip
	pip install --upgrade google-api-python-client
	pip install bs4
	pip install wheel
	pip install lxml

# Настройка прав доступа для CGI-скриптов
setup-cgi:
	@echo "Установка прав доступа для CGI-скриптов..."
	chmod +x cgi-bin/*.py
	ls -la cgi-bin/
	@echo "Права доступа установлены. Теперь вы можете запустить сервер."

# Запуск локального веб-сервера с поддержкой CGI
run:
	@echo "Запуск локального HTTP веб-сервера с поддержкой CGI на порту 8000..."
	@echo "Откройте страницу загрузки файлов: http://localhost:8000/cgi-bin/upload.py"
	@echo "ИЛИ (если вы используете WAMP/OSPanel): http://timelogger/cgi-bin/upload.py"
	python3 -m http.server --cgi 8000

# Запуск всех тестов из папки /tests
test:
	@echo "Запуск тестов..."
	python3 -m pytest tests/ -v
	@echo "Тесты завершены"
