import pandas as pd


def category_expenses(transactions, category, date=None):
    """Возращает траты по категории за последние три месяца"""
    if date is None:
        date = pd.Timestamp.today()

    date = pd.Timestamp(date)
    start_date = date - pd.DateOffset(months=3)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="mixed", dayfirst=True,)

    expenses = transactions[
        (transactions["Категория"].str.lower() == category.lower())
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
        & (transactions["Сумма операции"] < 0)
    ]
    return expenses
