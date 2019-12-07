CREATE TABLE monthly_budget AS
SELECT DISTINCT
    c.konto [konto],
    date(c.data, 'Start of month') [data],
    IFNULL(c.kategoria, 'BLANK') [kategoria],
    IFNULL(c.subkategoria, 'BLANK') [subkategoria],
    CAST(SUM(IFNULL(c."min", 0)) AS REAL) [min],
    CAST(SUM(IFNULL(c."avg", 0)) AS REAL) [avg],
    CAST(SUM(IFNULL(c."max", 0)) AS REAL) [max]
FROM cashflow_details c
GROUP BY c.konto, date(c.data, 'Start of month'),IFNULL(c.kategoria, 'BLANK'), IFNULL(c.subkategoria, 'BLANK')
ORDER BY 1 ASC, 2 ASC, 3 ASC, 4 ASC