from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

class Config:
    SECRET_KEY = 'your-secret-key-here'
    DATA_FILES = {
        'clients': 'data/clients.csv',
        'hot_leads': 'data/hot_leads.xlsx',
        'crypto_images': 'data/crypto-images'
    }
    MOCK_DATA = True