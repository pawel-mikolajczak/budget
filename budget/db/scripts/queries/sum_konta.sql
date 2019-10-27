CREATE TABLE sum_konta as
SELECT
    DATE(data, 'Start of month') [miesiac],
    konto,
    SUM(kwota) [suma]
FROM konta
GROUP BY DATE(data, 'Start of month'), konto
ORDER BY 1 DESC, 2 ASC