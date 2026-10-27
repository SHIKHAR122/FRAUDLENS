import sqlite3
import pandas as pd
from config import DB_PATH
from velocity import get_velocity_flags
from statistical_featues import add_statistical_flags

conn = sqlite3.connect(DB_PATH)
base = pd.read_sql_query(
    "SELECT * FROM transactions WHERE type IN ('TRANSFER', 'CASH_OUT')", conn
)
conn.close()

velocity_df = get_velocity_flags()
flagged = add_statistical_flags(base)

merged = flagged.merge(
    velocity_df[['nameDest', 'step', 'velocity_flag']],
    on=['nameDest', 'step'], how='left'
)
merged['velocity_flag'] = merged['velocity_flag'].fillna(False)

merged['risk_score'] = (
    merged['velocity_flag'].astype(int) +
    merged['z_flag'].astype(int) +
    merged['iqr_flag'].astype(int)
)

merged['risk_score'] = (
    merged['z_flag'].astype(int) +
    merged['iqr_flag'].astype(int)
)

print('--- Mean risk score by isFraud (velocity excluded) ---')
print(merged.groupby('isFraud')['risk_score'].mean())

print('\n--- Would flagging risk_score >= 1 catch fraud? ---')
merged['flagged_any'] = merged['risk_score'] >= 1
print(pd.crosstab(merged['isFraud'], merged['flagged_any']))

print('\n--- Would flagging risk_score >= 2 (both signals agree) catch fraud? ---')
merged['flagged_both'] = merged['risk_score'] >= 2
print(pd.crosstab(merged['isFraud'], merged['flagged_both']))

print('--- Mean risk score by isFraud ---')
print(merged.groupby('isFraud')['risk_score'].mean())

print('\n--- Would flagging risk_score >= 1 catch fraud? ---')
merged['flagged_any'] = merged['risk_score'] >= 1
print(pd.crosstab(merged['isFraud'], merged['flagged_any']))