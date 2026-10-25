from unittest.mock import Mock, patch

import pandas as pd

from src.services import get_currency_rates, get_stock_prices, simple_search


def test_simple_search() -> None:
    """Проверяем поиск транзакции по категории и описанию."""
    transactions = pd.DataFrame(
        [
            {
                "Категория": "Супермаркеты",
                "Описание": "Пятерочка",
            },
            {
                "Категория": "Транспорт",
                "Описание": "Такси",
            },
            {
                "Категория": "Кафе",
                "Описание": "Супермаркет рядом",
            },
        ]
    )
    result = simple_search("супермаркет", transactions)

    assert "Пятерочка" in result
    assert "Супермаркет рядом" in result
    assert "Такси" not in result

    result_upper = simple_search("супермаркет", transactions)
    assert "Пятерочка" in result_upper

    result_part = simple_search("маркет", transactions)
    assert "Супермаркет рядом" in result_part


@patch("src.services.requests.get")
def test_get_stock_prices(mock_get):
    """Проверяет получение цен акций без запросов к API."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "Global Quote": {
            "01. symbol": "AAPL",
            "05. price": "200.5000",
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with patch("src.services.os.getenv", return_value="test_api_key"):
        with patch("builtins.open") as mock_open:
            mock_open.return_value.__enter__return_value.read.return_value = '{"user_stocks": ["AAPL"]}'
            with patch("src.services.json.load", return_value={"user_stocks": ["AAPL"]}):
                result = get_stock_prices()

    assert result == [{"stock": "AAPL", "price": 200.5}]
    mock_get.assert_called_once()


@patch("src.services.requests.get")
def test_get_currency_rates(mock_get):
    """Проверяет получение курсов валют"""
    mock_get.return_value.content = b"""
    <ValCurs>
        <Valute><CharCode>USD</CharCode><Nominal>1</Nominal><Value>80,50</Value></Valute>
    </ValCurs>
    """
    result = get_currency_rates()
    assert result[0]["currency"] == "USD"
    assert result[0]["rate"] == 80.50
    mock_get.assert_called_once()
