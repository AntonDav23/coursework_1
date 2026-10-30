import json
from unittest.mock import patch

from src.views import hello, main_page


@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_main_page(mock_get_stock_prices, mock_get_currency_rates):
    """Проверяем формирование главной страницы."""
    mock_get_stock_prices.return_value = [
        {"stock": "AAPL", "price": 200.0},
        {"stock": "AMZN", "price": 190.0},
        {"stock": "GOOGL", "price": 170.0},
        {"stock": "MSFT", "price": 420.0},
        {"stock": "TSLA", "price": 250.0},
    ]

    mock_get_currency_rates.return_value = [
        {"currency": "USD", "rate": 80.5},
        {"currency": "EUR", "rate": 90.2},
    ]

    result = main_page("2021-12-21 14:30:00")
    data = json.loads(result)

    assert data["greeting"] == "Добрый день"
    assert len(data["top_transactions"]) == 5
    assert "cards" in data
    assert len(data["cards"]) == 1
    assert "currency_rates" in data
    assert isinstance(data["currency_rates"], list)
    assert len(data["currency_rates"]) > 0
    assert "stock_prices" in data
    assert isinstance(data["stock_prices"], list)
    assert len(data["stock_prices"]) == 5


def test_hello():
    """Проверяем приветствие в разное время суток."""
    assert hello(8) == "Доброе утро"
    assert hello(12) == "Добрый день"
    assert hello(18) == "Добрый вечер"
    assert hello(23) == "Доброй ночи"
