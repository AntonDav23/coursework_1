import pandas as pd

from src.services import simple_search


def test_simple_search():
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
