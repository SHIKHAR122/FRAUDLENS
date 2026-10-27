import pandas as pd
from config import Z_THRESHOLD, IQR_MULTIPLIER

def add_statistical_flags(df):
    df = df[df['type'].isin(['TRANSFER', 'CASH_OUT'])].copy()

    stats = df.groupby('nameDest')['amount'].agg(['mean', 'std']).rename(
        columns={'mean': 'dest_mean', 'std': 'dest_std'}
    )
    df = df.merge(stats, on='nameDest', how='left')
    df['zscore'] = (df['amount'] - df['dest_mean']) / df['dest_std']
    df['z_flag'] = (df['zscore'].abs() > Z_THRESHOLD).fillna(False)

    q = df.groupby('nameDest')['amount'].quantile([0.25, 0.75]).unstack()
    q.columns = ['Q1', 'Q3']
    q['IQR'] = q['Q3'] - q['Q1']
    q['lower'] = q['Q1'] - IQR_MULTIPLIER * q['IQR']
    q['upper'] = q['Q3'] + IQR_MULTIPLIER * q['IQR']
    df = df.merge(q[['lower', 'upper']], on='nameDest', how='left')
    df['iqr_flag'] = ((df['amount'] < df['lower']) | (df['amount'] > df['upper'])).fillna(False)

    return df

if __name__ == '__main__':
    import sqlite3
    from config import DB_PATH

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query('SELECT * FROM transactions', conn)
    conn.close()

    flagged = add_statistical_flags(df)

    print('--- Flag counts ---')
    print(flagged[['z_flag', 'iqr_flag']].sum())

    print('\n--- Z-flag rate by isFraud ---')
    print(flagged.groupby('isFraud')['z_flag'].mean())

    print('\n--- IQR-flag rate by isFraud ---')
    print(flagged.groupby('isFraud')['iqr_flag'].mean())