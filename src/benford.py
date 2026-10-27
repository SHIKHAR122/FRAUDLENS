import numpy as np
import pandas as pd
import sqlite3
from config import DB_PATH

def benfords_expected():
    return {d: np.log10(1 + 1/d) for d in range(1, 10)}

def leading_digit(amount):
    s = str(int(abs(amount)))
    return int(s[0]) if s and s[0] != '0' else None

def benford_chi_square(amounts):
    digits = amounts.apply(leading_digit).dropna()
    observed = digits.value_counts(normalize=True).sort_index()
    expected = benfords_expected()

    chi_sq = 0
    n = len(digits)
    for d in range(1, 10):
        obs_count = observed.get(d, 0) * n
        exp_count = expected[d] * n
        chi_sq += ((obs_count - exp_count) ** 2) / exp_count

    return chi_sq / n   # <-- normalized, per-record deviation

if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM transactions WHERE type IN ('TRANSFER', 'CASH_OUT')", conn
    )
    conn.close()

    print('--- Normalized chi-square: all transactions ---')
    print(benford_chi_square(df['amount']))

    print('\n--- Normalized chi-square: fraud only ---')
    print(benford_chi_square(df[df['isFraud'] == 1]['amount']))

    print('\n--- Normalized chi-square: non-fraud only ---')
    print(benford_chi_square(df[df['isFraud'] == 0]['amount']))