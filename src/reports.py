import pandas as pd
from typing import Any


def category_expenses(transactions: pd.DataFrame, category: str, date: Any = None) -> pd.DataFrame:
    """Возращает траты по категории за последние три месяца"""
    if date is None:
        date = pd.Timestamp.today()

    date = pd.Timestamp(date)
    start_date = date - pd.DateOffset(months=3)

    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        format="mixed",
        dayfirst=True,
    )

    expenses: pd.DataFrame = transactions[
        (transactions["Категория"].str.lower() == category.lower())
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
        & (transactions["Сумма операции"] < 0)
    ]
    return expenses
