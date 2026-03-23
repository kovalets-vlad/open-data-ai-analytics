import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

def main():
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:admin@db:5432/equipment_db")
    engine = create_engine(db_url)
    
    print("Зчитування даних для генерації графіків...")
    df = pd.read_sql("SELECT * FROM equipment_data", engine)

    output_dir = '/app/plots'
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # Гіпотеза 1
    plt.figure(figsize=(10, 6))
    plot_data = df.dropna(subset=['equipment_age', 'wearPercentage'])
    if not plot_data.empty:
        sns.scatterplot(data=plot_data, x='equipment_age', y='wearPercentage', alpha=0.3, color='royalblue')
        plt.title('Equipment Age vs Wear Percentage')
        plt.savefig(os.path.join(output_dir, 'hypothesis_1_age_vs_wear.png'))
    plt.close()

    # Гіпотеза 2
    if 'serviceSubgroupTitle' in df.columns:
        df_copy = df.copy()
        df_copy['serviceSubgroupTitle'] = df_copy['serviceSubgroupTitle'].fillna('Unknown')
        top_subgroups = df_copy.groupby('serviceSubgroupTitle')['primaryAmountValue'].sum().sort_values(ascending=False).head(10)
        
        plt.figure(figsize=(12, 7))
        sns.barplot(x=top_subgroups.values, y=top_subgroups.index, hue=top_subgroups.index, palette='viridis', legend=False)
        plt.title('Asset Structure (Top 10 Subgroups)')
        plt.savefig(os.path.join(output_dir, 'hypothesis_2_top_10_subgroups.png'))
    plt.close()

    print(f"✅ Графіки успішно збережено у {output_dir}")

if __name__ == "__main__":
    main()