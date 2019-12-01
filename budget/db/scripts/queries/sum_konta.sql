CREATE TABLE sum_konta as
SELECT
    DATE(data, 'Start of month') [miesiac],
    konto,
    CAST(SUM(kwota) AS REAL) [suma]
FROM konta
GROUP BY DATE(data, 'Start of month'), konto
ORDER BY 1 DESC, 2 ASC