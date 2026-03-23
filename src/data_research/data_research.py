import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

def conduct_research(df: pd.DataFrame, report_path: str = 'artifacts/research_report.json') -> dict:

    report = {}

    numeric_cols = ['primaryAmountValue', 'wearPercentage', 'equipment_age', 'bookAmountValue']
    existing_cols = [col for col in numeric_cols if col in df.columns]
    report['descriptive_statistics'] = df[existing_cols].describe().to_dict()

    ml_df = df.dropna(subset=['bookAmountValue', 'equipment_age', 'wearPercentage']).copy()
    
    if not ml_df.empty:
        features = ['primaryAmountValue', 'wearPercentage', 'equipment_age', 'serviceSubgroupTitle', 'producerName']
        X = ml_df[features].copy()
        y = ml_df['bookAmountValue']

        X['producerName'] = X['producerName'].fillna('Unknown')
        for col in ['serviceSubgroupTitle', 'producerName']:
            X[col] = pd.factorize(X[col])[0]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_regressor.fit(X_train, y_train)
        y_pred = rf_regressor.predict(X_test)

        report['ml_results'] = {
            'r2_score': round(r2_score(y_test, y_pred), 4),
            'mean_absolute_error_uah': round(mean_absolute_error(y_test, y_pred), 2)
        }
    
    import os
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
        
    print(f"\n--- Результати дослідження збережено у {report_path} ---")
    
    return report

if __name__ == "__main__":
    import sqlite3
    import os

    db_path = "equipment.db"
    if os.path.exists(db_path):
        print("Запуск data_research.py: тренування моделі та генерація звіту...")
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql("SELECT * FROM equipment_data", conn)
        
        conduct_research(df)
    else:
        print(f"❌ Помилка: Базу даних {db_path} не знайдено. Спочатку запустіть data_load.py")