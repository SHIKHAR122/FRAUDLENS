import pandas as pd
import sqlite3
import os
from config import DB_PATH, CSV_PATH, SAMPLE_SIZE

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

df = pd.read_csv(CSV_PATH, nrows=SAMPLE_SIZE)

conn = sqlite3.connect(DB_PATH)
df.to_sql('transactions', conn, if_exists='replace', index=False)
conn.commit()
conn.close()
print(f'Loaded {len(df)} rows into {DB_PATH}')