CREATE TABLE monthly_budget AS
SELECT DISTINCT
    date(c.data, 'Start of month') [data],
    IFNULL(c.kategoria, 'BLANK') [kategoria],
    IFNULL(c.subkategoria, 'BLANK') [subkategoria],
    SUM(IFNULL(c."min", 0)) [min],
    SUM(IFNULL(c."avg", 0)) [avg],
    SUM(IFNULL(c."max", 0)) [max]
FROM cashflow_details c
GROUP BY date(c.data, 'Start of month'),IFNULL(c.kategoria, 'BLANK'), IFNULL(c.subkategoria, 'BLANK')
ORDER BY 1 ASC, 2 ASC, 3 ASC