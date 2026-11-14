-- SQLite-compatible starter analysis. Import upi_cleaned.csv as table upi_transactions.
SELECT fraud_flag, COUNT(*) AS transaction_count
FROM upi_transactions GROUP BY fraud_flag;

SELECT transaction_type, COUNT(*) AS total_transactions,
       SUM(fraud_flag) AS fraud_transactions,
       ROUND(100.0 * SUM(fraud_flag) / COUNT(*), 2) AS fraud_rate_pct
FROM upi_transactions GROUP BY transaction_type ORDER BY fraud_rate_pct DESC;

SELECT sender_state, COUNT(*) AS total_transactions,
       SUM(fraud_flag) AS fraud_transactions
FROM upi_transactions GROUP BY sender_state ORDER BY fraud_transactions DESC;

SELECT fraud_flag, ROUND(AVG(amount_inr),2) AS average_amount
FROM upi_transactions GROUP BY fraud_flag;

SELECT hour_of_day, COUNT(*) AS transactions, SUM(fraud_flag) AS fraud_count
FROM upi_transactions GROUP BY hour_of_day ORDER BY hour_of_day;
