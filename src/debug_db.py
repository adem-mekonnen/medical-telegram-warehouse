import os
from dotenv import load_dotenv
import psycopg2

# Force reload of .env
load_dotenv(override=True)

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

print("--- DEBUG INFO ---")
print(f"User: '{user}'")
print(f"Password: '{password}'")  # We need to see if this is empty
print(f"Host: '{host}'")
print(f"Port: '{port}'")
print("------------------")

try:
    conn = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        dbname=dbname
    )
    print("✅ SUCCESS! Connected to database.")
    conn.close()
except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")