import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

df = pd.read_csv('open-data-ai-analytics/data/raw/medical_data.csv')

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