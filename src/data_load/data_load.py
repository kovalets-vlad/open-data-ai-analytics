import os
import pandas as pd
from sqlalchemy import create_engine

def main():
    csv_path = '/app/data/raw/equipment_data.csv'
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:admin@db:5432/equipment_db")
    
    print(f"Починаємо завантаження даних з {csv_path}...")
    
    if not os.path.exists(csv_path):
        print(f"❌ Помилка: Файл {csv_path} не знайдено!")
        return

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

    engine = create_engine(db_url)
    df.to_sql('equipment_data', engine, if_exists='replace', index=False)
    
    print("✅ Дані успішно очищено та завантажено в базу даних PostgreSQL!")

if __name__ == "__main__":
    main()