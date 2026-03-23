import pandas as pd
import sqlite3

def load_and_preprocess_data(csv_path: str, db_path: str = "equipment.db", table_name: str = "equipment_data") -> pd.DataFrame:
    """Читає CSV, очищає дані та зберігає їх у базу даних."""
    
    df = pd.read_csv(csv_path)

    df['dateReceived'] = pd.to_datetime(df['dateReceived'], errors='coerce')

    cols_to_fix = ['primaryAmountValue', 'amortizationAmountValue', 'bookAmountValue', 'wearPercentage']
    for col in cols_to_fix:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce')

    df = df.drop_duplicates().reset_index(drop=True)

    current_year = 2026
    df['year_received'] = df['dateReceived'].dt.year
    df['equipment_age'] = current_year - df['year_received']

    mask = df['wearPercentage'].isna() & (df['primaryAmountValue'] > 0)
    df.loc[mask, 'wearPercentage'] = (df['amortizationAmountValue'] / df['primaryAmountValue']) * 100

    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"--- Дані успішно завантажено у таблицю '{table_name}' БД '{db_path}' ---")

    return df

if __name__ == "__main__":
    import os
    csv_path = 'open-data-ai-analytics/data/raw/equipment_data.csv'
    
    if os.path.exists(csv_path):
        print(f"Запуск data_load.py: обробка файлу {csv_path}...")
        load_and_preprocess_data(csv_path)
    else:
        print(f"❌ Помилка: Файл {csv_path} не знайдено. Спочатку переконайтеся, що відпрацював get_data.py")