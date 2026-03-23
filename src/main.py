from data_load.data_load import load_and_preprocess_data
from data_quality_analysis.data_quality_analysis import analyze_data_quality
from data_research.data_research import conduct_research
from visualization.visualization import create_visualizations

def main():
    csv_path = 'open-data-ai-analytics/data/raw/equipment_data.csv'
    
    df = load_and_preprocess_data(csv_path)
    
    analyze_data_quality(df)
    
    conduct_research(df)
    
    create_visualizations(df)

if __name__ == "__main__":
    main()