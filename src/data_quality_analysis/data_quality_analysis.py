import os
import json
import pandas as pd
from sqlalchemy import create_engine

def main():
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:admin@db:5432/equipment_db")
    engine = create_engine(db_url)
    
    print("Зчитування даних з БД для аналізу якості...")
    df = pd.read_sql("SELECT * FROM equipment_data", engine)

    missing_data = df.isnull().sum().to_dict()
    missing_percent = ((df.isnull().sum() / len(df)) * 100).round(2).to_dict()
    duplicates = int(df.duplicated().sum())
    total_rows = len(df)

    # Формуємо звіт
    report = {
        "total_rows": total_rows,
        "duplicates": duplicates,
        "columns_quality": {}
    }
    
    for col in df.columns:
        report["columns_quality"][col] = {
            "missing_values": int(missing_data[col]),
            "missing_percentage": float(missing_percent[col])
        }

    # Зберігаємо у спільний том
    os.makedirs('/app/reports', exist_ok=True)
    report_path = '/app/reports/quality_report.json'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Звіт про якість даних збережено у {report_path}")

if __name__ == "__main__":
    main()