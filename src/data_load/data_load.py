import os
import pandas as pd
from sqlalchemy import create_engine

def clean_equipment_data(df):
    df['dateReceived'] = pd.to_datetime(df['dateReceived'], errors='coerce')
    
    cols_to_fix = ['primaryAmountValue', 'amortizationAmountValue', 'bookAmountValue', 'wearPercentage']
    for col in cols_to_fix:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), 
                errors='coerce'
            )

    current_year = 2026
    df['year_received'] = df['dateReceived'].dt.year
    df['equipment_age'] = current_year - df['year_received']
    
    df = df[(df['equipment_age'] >= 0) & (df['equipment_age'] <= 100)]
    
    mask = df['wearPercentage'].isna() & (df['primaryAmountValue'] > 0)
    df.loc[mask, 'wearPercentage'] = (df['amortizationAmountValue'] / df['primaryAmountValue']) * 100
    
    df = df[(df['wearPercentage'] >= 0) & (df['wearPercentage'] <= 100)]

    for col in ['primaryAmountValue']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    if 'serviceSubgroupTitle' in df.columns:
        df['serviceSubgroupTitle'] = df['serviceSubgroupTitle'].str.strip().str.capitalize().fillna('Unknown')

    return df.drop_duplicates().reset_index(drop=True)

def main():
    csv_path = '/app/data/raw/equipment_data.csv'
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:admin@db:5432/equipment_db")
    
    if not os.path.exists(csv_path):
        print(f"❌ Файл {csv_path} не знайдено!")
        return

    df_raw = pd.read_csv(csv_path)
    df = clean_equipment_data(df_raw)

    engine = create_engine(db_url)
    df.to_sql('equipment_data', engine, if_exists='replace', index=False)
    
    print(f"✅ Очищено! Залишилось {len(df)} рядків з {len(df_raw)}.")

if __name__ == "__main__":
    main()