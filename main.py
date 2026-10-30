import json

from src.views import main_page


def main() -> None:
    """Запускаем главную страницу приложения."""
    data_string = "2021-12-21 14:30:00"

    result = main_page(data_string)
    data = json.loads(result)

    print(json.dumps(data, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
