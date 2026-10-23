from datetime import datetime
from src.utils import load_transactions
import json
import pandas as pd


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
    greeting = get_greeting(date_string)
    transactions = load_transactions()

    # информация об одной банковской карте
    card_transactions = transactions[transactions["Номер карты"] == "*7197"]

    card_info = {
        "last_digits": "*7197",
        "total_transactions": len(card_transactions),
    }

    # топ-5 транзакций по сумме платежа
    top_transactions = transactions.sort_values(by="Сумма платежа", ascending=False).head(5)
    top_transactions = top_transactions[["Дата операции", "Сумма платежа", "Категория", "Описание"]]
    top_transactions["Дата операции"] = pd.to_datetime(top_transactions["Дата операции"], dayfirst=True).dt.strftime(
        "%d.%m.%Y"
    )

    result = {
        "greeting": greeting,
        "top_transactions": top_transactions.to_dict(orient="records"),
        "card_info": card_info,
    }

    return json.dumps(result, ensure_ascii=False, default=str)
