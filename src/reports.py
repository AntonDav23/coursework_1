from functools import wraps
from typing import Any, Callable

import pandas as pd


def save_report(filename: str="report.json") -> Callable:
    """Декоратор для сохранения результата отчета в JSON-файл."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            result.to_json(
                filename,
                orient="records",
                force_ascii=False,
                indent=4,
                date_format="iso",
            )
            return result

        return wrapper

    return decorator


@save_report()
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
