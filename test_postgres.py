import os

import psycopg
from dotenv import load_dotenv


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is not configured")


with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        result = cur.fetchone()

print("PostgreSQL connection successful!")
print(result[0])