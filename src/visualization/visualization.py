import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

def create_visualizations(df: pd.DataFrame, output_dir: str = 'artifacts/sample_analysis'):
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")
    
    plt.figure(figsize=(10, 6))
    plot_data = df.dropna(subset=['equipment_age', 'wearPercentage'])
    if not plot_data.empty:
        sns.scatterplot(data=plot_data, x='equipment_age', y='wearPercentage', alpha=0.3, color='royalblue')
        plt.title('Hypothesis 1: Equipment Age vs Wear Percentage')
        plt.savefig(os.path.join(output_dir, 'hypothesis_1_age_vs_wear.png'))
    plt.close()

    if 'serviceSubgroupTitle' in df.columns:
        df_copy = df.copy()
        df_copy['serviceSubgroupTitle'] = df_copy['serviceSubgroupTitle'].fillna('Unknown')
        top_subgroups = df_copy.groupby('serviceSubgroupTitle')['primaryAmountValue'].sum().sort_values(ascending=False).head(10)
        
        plt.figure(figsize=(12, 7))
        sns.barplot(x=top_subgroups.values, y=top_subgroups.index, hue=top_subgroups.index, palette='viridis', legend=False)
        plt.title('Hypothesis 2: Asset Structure (Top 10 Subgroups)')
        plt.savefig(os.path.join(output_dir, 'hypothesis_2_top_10_subgroups.png'))
    plt.close()

    print(f"--- Графіки успішно збережено у {output_dir} ---")

if __name__ == "__main__":
    import sqlite3
    import os

    db_path = "equipment.db"
    if os.path.exists(db_path):
        print("Запуск visualization.py: створення графіків...")
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql("SELECT * FROM equipment_data", conn)
        
        create_visualizations(df)
    else:
        print(f"❌ Помилка: Базу даних {db_path} не знайдено. Спочатку запустіть data_load.py")