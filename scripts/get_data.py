import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def download_data():
    url = "https://data.gov.ua/dataset/41cb520d-95d8-4c5c-baad-9d4177618ace/resource/400a1681-6535-43fa-b76c-d27efc348773/download/equipment_2025-12-15.csv" 
    save_path = "open-data-ai-analytics/data/raw/equipment_data.csv"
    
    if not os.path.exists('open-data-ai-analytics/data/raw'):
        os.makedirs('open-data-ai-analytics/data/raw')

    # Налаштовуємо автоматичні повтори (Retries)
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        print("Починаємо завантаження (режим стрімінгу)...")
        # stream=True дозволяє завантажувати файл частинами
        with session.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk: 
                        f.write(chunk)
        print(f"✅ Дані успішно збережено: {save_path}")
    except Exception as e:
        print(f"❌ Помилка завантаження: {e}")

if __name__ == "__main__":
    download_data()