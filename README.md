![Skypro](https://static.tildacdn.com/tild3364-3965-4237-b664-363533643431/Group_1321317003.svg)

**COURSEWORK_1**  
"Анализ банковских операций"

1. Описание проекта
Проект предназначен для обработки и анализа банковских транзакций их Excel-файла. 
2. Реализованные возможности:
 - загрузка банковских транзакций из файла, 
 - вывод информации одной банковской карты,
 - вывод пяти транзакций с датой, суммой операции, категорией и описанием,
 - форматирование приветствия в зависимости от времени суток, 
 - форматирование отчетов по расходам, 
 - форматирование результата в формате json.
3. Структура проекта:  
├── src   
│ ├── __init__.py  
│ ├── utils.py  
│ ├── views.py  
│ ├── reports.py  
│ └── services.py  
├── data  
│ ├── operations.xlsx  
├── tests  
│ ├── __init__.py  
│ ├── test_views.py  
│ ├── test_reports.py  
│ └── test_services.py  
├── user_settings.json  
├── .env  
├── .flake8  
├── .gitignore  
├── pyproject.toml  
├── poetry.lock  
└── README.md  
4. Запуск приложения  
python main.py
5. Запуск тестирования  
pytest -v

## Лицензия.
Этот проект распространяется под лицензией MIT.  

<p style="text-align: center;">Developed with ❤️ by A.Davydov</p>