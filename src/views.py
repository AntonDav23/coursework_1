import json
from datetime import datetime

import pandas as pd

from src.services import get_currency_rates, get_stock_prices
from src.utils import load_transactions


def hello(hour: int) -> str:
    """Возвращаем приветствие в зависимости от времени суток."""
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_greeting(data_string: str) -> str:
    """Получает строку с датой и временем и возвращает приветствие."""
    date_time = datetime.strptime(data_string, "%Y-%m-%d %H:%M:%S")
    return hello(date_time.hour)


def main_page(date_string: str) -> str:
    """Формирует данные для главной страницы."""
    date_time = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    greeting = hello(date_time.hour)
    transactions = load_transactions()

    # Оставляем операции с первого числа месяца по переданному дату
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    start_date = date_time.replace(day=1, hour=0, minute=0, second=0)
    transactions = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= date_time)
    ].copy()

    # информация об одной банковской карте
    card_transactions = transactions[transactions["Номер карты"] == "*7197"]

    expenses = card_transactions[card_transactions["Сумма платежа"] < 0]
    total_spent = -expenses["Сумма платежа"].sum()

    card_info = {
        "last_digits": "7197",
        "total_spent": round(total_spent, 2),
        "cashback": round(total_spent // 100, 2),
        "total_transactions": len(card_transactions),
    }

    # топ-5 транзакций по сумме платежа
    top_transactions = transactions.sort_values(by="Сумма платежа", ascending=False).head(5)
    top_transactions = top_transactions[["Дата операции", "Сумма платежа", "Категория", "Описание"]]
    top_transactions["Дата операции"] = pd.to_datetime(top_transactions["Дата операции"], dayfirst=True).dt.strftime(
        "%d.%m.%Y"
    )
    top_transactions = top_transactions.rename(
        columns={
            "Дата операции": "date",
            "Сумма платежа": "amount",
            "Категория": "category",
            "Описание": "discription",
        }
    )

    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices()

    result = {
        "greeting": greeting,
        "top_transactions": top_transactions.to_dict(orient="records"),
        "cards": [card_info],
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(result, ensure_ascii=False, default=str)
