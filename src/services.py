import json


def simple_search(query, transactions):
    """Ищет транзакции по категориии или описанию"""
    query = query.lower()
    result = []
    for _, transaction in transactions.iterrows():
        category = str(transaction["Категория"]).lower()
        description = str(transaction["Описание"]).lower()

        if query in category or query in description:
            result.append(transaction.to_dict())
    return json.dumps(result, ensure_ascii=False, default=str)

