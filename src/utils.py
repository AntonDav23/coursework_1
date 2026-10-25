from pathlib import Path

import pandas as pd


def load_transactions() -> pd.DataFrame:
    """Загружаем транзакции из Excel-файла."""
    project_dir = Path(__file__).resolve().parent.parent
    file_path = project_dir / "data" / "operations.xlsx"
    return pd.read_excel(file_path)
