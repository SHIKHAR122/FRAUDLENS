SELECT
    nameDest, step, amount, isFraud, type,
    COUNT(*) OVER (
        PARTITION BY nameDest
        ORDER BY step
        RANGE BETWEEN CURRENT ROW AND CURRENT ROW
    ) AS txn_count_window
FROM transactions
WHERE type IN ('TRANSFER', 'CASH_OUT');