import os
import json
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

def main():
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:admin@db:5432/equipment_db")
    engine = create_engine(db_url)
    
    print("Зчитування даних для дослідження та ML...")
    df = pd.read_sql("SELECT * FROM equipment_data", engine)

    report = {}
    
    # 1. Статистики
    numeric_cols = ['primaryAmountValue', 'wearPercentage', 'equipment_age', 'bookAmountValue']
    existing_cols = [col for col in numeric_cols if col in df.columns]
    report['descriptive_statistics'] = df[existing_cols].describe().to_dict()

    # 2. Модель ML
    ml_df = df.dropna(subset=['bookAmountValue', 'equipment_age', 'wearPercentage']).copy()
    if not ml_df.empty:
        features = ['primaryAmountValue', 'wearPercentage', 'equipment_age', 'serviceSubgroupTitle', 'producerName']
        X = ml_df[features].copy()
        y = ml_df['bookAmountValue']

        X['producerName'] = X['producerName'].fillna('Unknown')
        for col in ['serviceSubgroupTitle', 'producerName']:
            X[col] = pd.factorize(X[col])[0]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)

        report['ml_results'] = {
            'r2_score': round(r2_score(y_test, y_pred), 4),
            'mean_absolute_error_uah': round(mean_absolute_error(y_test, y_pred), 2)
        }

    os.makedirs('/app/reports', exist_ok=True)
    report_path = '/app/reports/research_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Результати дослідження збережено у {report_path}")

if __name__ == "__main__":
    main()