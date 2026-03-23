import pandas as pd

def analyze_data_quality(df: pd.DataFrame) -> pd.DataFrame:
    
    missing_data = df.isnull().sum()
    missing_percent = (df.isnull().sum() / len(df)) * 100
    duplicates = df.duplicated().sum()
    unique_values = df.nunique()

    quality_report = pd.DataFrame({
        'Missing Values': missing_data,
        'Percentage (%)': missing_percent.round(2),
        'Unique Values': unique_values,
        'Data Type': df.dtypes
    })

    print("\n--- Звіт про якість даних ---")
    print(f"Загальна кількість рядків: {len(df)}")
    print(f"Знайдено повних дублікатів: {duplicates}")
    print("\nДеталізація по колонках:")
    print(quality_report)

    if 'dateReceived' in df.columns:
        nat_counts = df['dateReceived'].isna().sum()
        if nat_counts > 0:
            print(f"\n⚠️ Увага: {nat_counts} дат не вдалося розпізнати (стали NaT).")

    return quality_report

if __name__ == "__main__":
    import os
    import sqlite3

    db_path = "equipment.db"
    if os.path.exists(db_path):
        print("Запуск data_quality_analysis.py: читання БД...")
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql("SELECT * FROM equipment_data", conn)
        
        analyze_data_quality(df)
    else:
        print(f"❌ Помилка: Базу даних {db_path} не знайдено. Спочатку запустіть data_load.py")