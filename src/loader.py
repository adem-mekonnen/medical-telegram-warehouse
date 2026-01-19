import os
import json
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# DB Connection
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URL)

def load_raw_json():
    base_path = "data/raw/telegram_messages"
    all_data = []

    # Walk through the data lake
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_data.extend(data)

    if not all_data:
        print("No data found to load.")
        return

    # Convert to Pandas DataFrame
    df = pd.DataFrame(all_data)

    # Ensure raw schema exists
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()

    # Load to PostgreSQL
    df.to_sql('telegram_messages', engine, schema='raw', if_exists='replace', index=False)
    print(f"Successfully loaded {len(df)} rows into raw.telegram_messages")

if __name__ == "__main__":
    load_raw_json()