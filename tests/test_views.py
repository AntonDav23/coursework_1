import json
import pandas as pd

from src.views import main_page, hello


def test_main_page():
    """Проверяем формирование главной страницы."""
    result = main_page("2021-12-21 14:30:00")

    data = json.loads(result)

    assert data["greeting"] == "Добрый день"
    assert len(data["top_transactions"]) == 5
    assert "card_info" in data

def test_hello():
    """Проверяем приветствие в разное время суток."""
    assert hello(8) == "Доброе утро"
    assert hello(12) == "Добрый день"
    assert hello(18) == "Добрый вечер"
    assert hello(23) == "Доброй ночи"

