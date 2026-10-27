import sqlite3
import pandas as pd
from config import DB_PATH, VELOCITY_COUNT_THRESHOLD

def get_velocity_flags():
    conn = sqlite3.connect(DB_PATH)
    query = open('queries/velocity_queries.sql').read()
    df = pd.read_sql_query(query, conn)
    df['velocity_flag'] = df['txn_count_window'] >= VELOCITY_COUNT_THRESHOLD
    conn.close()
    return df

if __name__ == '__main__':
    result = get_velocity_flags()
    print(result['velocity_flag'].value_counts())
    print(result[result['velocity_flag']].head(10))
    print(result.groupby('isFraud')['velocity_flag'].mean())
