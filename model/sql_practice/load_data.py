# sql_practice/load_data.py
# Loads spam.csv into PostgreSQL

import pandas as pd
import psycopg2
from psycopg2 import sql

# ── Connection details — update with YOUR password ──────────
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "spam_testing_db",
    "user": "postgres",
    "password": "admin@123"   # ← the one you set during install
}

# ── Step 1: Load the CSV ─────────────────────────────────────
df = pd.read_csv('data/spam.csv', encoding='latin-1')
df = df[['v1', 'v2']]
df.columns = ['label', 'message']
df['msg_length'] = df['message'].apply(len)

print(f"Loaded {len(df)} rows from CSV")

# ── Step 2: Connect to PostgreSQL ────────────────────────────
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()
print("✅ Connected to PostgreSQL")

# ── Step 3: Create the table ─────────────────────────────────
cur.execute("""
    DROP TABLE IF EXISTS messages;
    CREATE TABLE messages (
        id SERIAL PRIMARY KEY,
        label VARCHAR(10),
        message TEXT,
        msg_length INTEGER
    );
""")
conn.commit()
print("✅ Table 'messages' created")

# ── Step 4: Insert the data ──────────────────────────────────
for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO messages (label, message, msg_length) VALUES (%s, %s, %s)",
        (row['label'], row['message'], row['msg_length'])
    )

conn.commit()
print(f"✅ Inserted {len(df)} rows into the database")

cur.close()
conn.close()
print("\n🎉 Done! Your spam data is now in PostgreSQL.")