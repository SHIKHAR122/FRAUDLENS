import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from config import DB_PATH
from benford import benfords_expected, leading_digit

def get_digit_distribution(amounts):
    digits = amounts.apply(leading_digit).dropna()
    observed = digits.value_counts(normalize=True).sort_index()
    # Ensure all digits 1-9 are present, even if count is 0
    return [observed.get(d, 0) for d in range(1, 10)]

if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM transactions WHERE type IN ('TRANSFER', 'CASH_OUT')", conn
    )
    conn.close()

    expected = benfords_expected()
    expected_values = [expected[d] for d in range(1, 10)]

    fraud_dist = get_digit_distribution(df[df['isFraud'] == 1]['amount'])
    nonfraud_dist = get_digit_distribution(df[df['isFraud'] == 0]['amount'])

    digits = list(range(1, 10))
    x = np.arange(len(digits))
    width = 0.25

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width, expected_values, width, label="Benford's expected", color='gray')
    ax.bar(x, nonfraud_dist, width, label='Non-fraud (observed)', color='steelblue')
    ax.bar(x + width, fraud_dist, width, label='Fraud (observed)', color='indianred')

    ax.set_xlabel('Leading digit')
    ax.set_ylabel('Proportion of transactions')
    ax.set_title("Benford's Law: expected vs observed leading-digit distribution")
    ax.set_xticks(x)
    ax.set_xticklabels(digits)
    ax.legend()
    plt.tight_layout()

    plt.savefig('docs/benford_comparison.png', dpi=150)
    print('Saved chart to docs/benford_comparison.png')
    plt.show()