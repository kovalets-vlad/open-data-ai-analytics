import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split 

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

df = pd.read_csv('open-data-ai-analytics/data/raw/equipment_data.csv')

missing_data = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df)) * 100

duplicates = df.duplicated().sum()

unique_values = df.nunique()

quality_report = pd.DataFrame({
    'Missing Values': missing_data,
    'Percentage (%)': missing_percent.round(2),
    'Unique Values': unique_values
})

print("--- Звіт про якість даних ---")
print(f"Загальна кількість рядків: {len(df)}")
print(f"Знайдено повних дублікатів: {duplicates}")
print("\nДеталізація по колонках:")
print(quality_report)


nat_counts = df['dateReceived'].isna().sum()
if nat_counts > 0:
    print(f"\n⚠️ Увага: {nat_counts} дат не вдалося розпізнати (стали NaT).")

df['dateReceived'] = pd.to_datetime(df['dateReceived'], errors='coerce')

cols_to_fix = ['primaryAmountValue', 'amortizationAmountValue', 'bookAmountValue', 'wearPercentage']

for col in cols_to_fix:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d.]', '', regex=True), errors='coerce')

# 2. Перетворення дати (як ми робили раніше)
df['dateReceived'] = pd.to_datetime(df['dateReceived'], errors='coerce')

# 3. Видалення дублікатів
df = df.drop_duplicates().reset_index(drop=True)

# 4. Тепер розрахунок маски спрацює без помилок
current_year = 2026
df['year_received'] = df['dateReceived'].dt.year
df['equipment_age'] = current_year - df['year_received']

# Розрахунок wearPercentage для тих рядків, де його немає
mask = df['wearPercentage'].isna() & (df['primaryAmountValue'] > 0)
df.loc[mask, 'wearPercentage'] = (df['amortizationAmountValue'] / df['primaryAmountValue']) * 100

print("Типи даних після виправлення:")
print(df[cols_to_fix].dtypes)

# Заповнюємо wearPercentage, якщо він порожній, використовуючи наявні суми
mask = df['wearPercentage'].isna() & (df['primaryAmountValue'] > 0)
df.loc[mask, 'wearPercentage'] = (df['amortizationAmountValue'] / df['primaryAmountValue']) * 100

# --- Візуалізація Гіпотез ---

# Гіпотеза 1: Age vs Wear
plt.figure(figsize=(10, 6))
plot_data = df.dropna(subset=['equipment_age', 'wearPercentage'])
sns.scatterplot(data=plot_data, x='equipment_age', y='wearPercentage', alpha=0.3, color='royalblue')
plt.title('Hypothesis 1: Equipment Age vs Wear Percentage')
plt.savefig('artifacts/analysis/hypothesis_1_age_vs_wear.png')
plt.close() # Очищає пам'ять

# Гіпотеза 2: Asset Structure
df['serviceSubgroupTitle'] = df['serviceSubgroupTitle'].fillna('Unknown')
top_subgroups = df.groupby('serviceSubgroupTitle')['primaryAmountValue'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 7))
sns.barplot(x=top_subgroups.values, y=top_subgroups.index, palette='viridis')
plt.title('Hypothesis 2: Asset Structure (Top 10 Subgroups)')
plt.savefig('artifacts/analysis/hypothesis_2_top_10_subgroups.png')
plt.close() # Очищає пам'ять

# --- 4. Побудова моделі (Machine Learning) ---

ml_df = df.dropna(subset=['bookAmountValue', 'equipment_age', 'wearPercentage']).copy()

features = ['primaryAmountValue', 'wearPercentage', 'equipment_age', 'serviceSubgroupTitle', 'producerName']
X = ml_df[features].copy()
y = ml_df['bookAmountValue']

# Заповнюємо текстові пропуски для моделі
X['producerName'] = X['producerName'].fillna('Unknown')

# Кодування категорій (перетворюємо текст на числа)
for col in ['serviceSubgroupTitle', 'producerName']:
    X[col] = pd.factorize(X[col])[0]

# Розподіл даних
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Навчання моделі
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train, y_train)

# Результати
y_pred = rf_regressor.predict(X_test)
print("\n--- Результати моделювання (Regression) ---")
print(f"R2 Score: {r2_score(y_test, y_pred):.4f}")
print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.2f} UAH")