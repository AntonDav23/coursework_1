import pandas as pd

from src.reports import category_expenses


def test_category_expenses():
    """Проверяем отбор расходов по категории и дате."""
    transactions = pd.DataFrame(
        [
            {
                "Дата операции": "2021-12-15",
                "Категория": "Супермаркеты",
                "Сумма операции": -500,
            },
            {
                "Дата операции": "2021-11-10",
                "Категория": "Супермаркеты",
                "Сумма операции": -300,
            },
            {
                "Дата операции": "2021-12-20",
                "Категория": "Транспорт",
                "Сумма операции": -100,
            },
            {
                "Дата операции": "2021-12-25",
                "Категория": "Супермаркеты",
                "Сумма операции": 200,
            },
        ]
    )

    result = category_expenses(transactions, category="Супермаркеты", date="2021-12-31")

    assert len(result) == 2
    assert all(result["Категория"] == "Супермаркеты")
    assert all(result["Сумма операции"] < 0)


def test_category_expenses_empty():
    """Проверяем категорию, по которой нет расходов."""
    transactions = pd.DataFrame(
        [
            {
                "Дата операции": "2021-12-15",
                "Категория": "Супермаркеты",
                "Сумма операции": -500,
            },
        ]
    )

    result = category_expenses(transactions, category="Транспорт", date="2021-12-31")
    assert len(result) == 0
