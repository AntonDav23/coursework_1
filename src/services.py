import json
import os
import xml.etree.ElementTree as ET

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


def simple_search(query: str, transactions: pd.DataFrame) -> str:
    """Ищет транзакции по категории или описанию"""
    query = query.lower()
    result = []
    for _, transaction in transactions.iterrows():
        category = str(transaction["Категория"]).lower()
        description = str(transaction["Описание"]).lower()

        if query in category or query in description:
            result.append(transaction.to_dict())
    return json.dumps(result, ensure_ascii=False, default=str)


def get_currency_rates() -> list[dict[str, str | float]]:
    """Получает курсы валют из API Центробанка России"""
    with open("user_settings.json", encoding="utf-8") as file:
        settings = json.load(file)

    currencies = settings["user_currencies"]

    url = "https://www.cbr.ru/scripts/XML_daily.asp"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    rates: list[dict[str, str | float]] = []

    for currency in root.findall("Valute"):
        code = currency.findtext("CharCode")
        if code is not None and code in currencies:
            nominal = int(currency.findtext("Nominal", "1"))
            value = float(currency.findtext("Value", default="0").replace(",", "."))
            rates.append({"currency": code, "rate": round(value / nominal, 2)})

    return rates


def get_stock_prices() -> list[dict[str, str | float]]:
    """Получаем цены акции через API AV."""
    with open("user_settings.json", encoding="utf-8") as file:
        settings = json.load(file)

    stocks = settings["user_stocks"]

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Не найден API_KEY в файле .env")

    url = "https://www.alphavantage.co/query"

    stock_prices = []

    for stock in stocks:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": stock,
            "apikey": api_key,
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "Error Massage" in data:
            raise ValueError(f"Ошибка при получении цены {stock}: " f"{data['Error Massage']}")

        if "Note" in data or "Information" in data:
            raise RuntimeError(f"AV ограничил запросы: " f"{data.get('Note', data.get('Information'))}")

        quote = data.get("Global Quote")
        if not quote or "05. price" not in quote:
            raise ValueError(f"API не вернул котировку для акции {stock}")

        price = float(quote["05. price"])

        if not price:
            raise ValueError("API не вернул цену для акции {stock}")

        stock_prices.append(
            {
                "stock": stock,
                "price": round(price, 2),
            }
        )

    return stock_prices
