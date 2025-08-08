# Experiments with regexp sanitization

import re
import pytest

def test_sanitize_time_string():
    """Test sanitizing time string by removing all characters except digits and :"""
    # Sanitize time string: leave only digits & ':' symbol
    s = "Example String 123 dfghdf:sdfgsd"
    expected = "123:"  # Ожидаемый результат - только цифры и двоеточие
    
    # Выполняем регулярное выражение
    replaced = re.sub('[^\d\:]', '', s)
    
    # Проверяем, что результат совпадает с ожидаемым
    assert replaced == expected, f"Expected '{expected}' but got '{replaced}'"
    
    # Дополнительный кейс
    s2 = "Test 12:34 time"
    expected2 = "1234:"
    replaced2 = re.sub('[^\d\:]', '', s2)
    assert replaced2 == expected2, f"Expected '{expected2}' but got '{replaced2}'"