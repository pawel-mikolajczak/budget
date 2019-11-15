SELECT date(c.data, 'Start of month') [data], SUM(c."min"*-1) [min], SUM(c."avg"*-1) [avg], SUM(c."max"*-1) [max]
FROM cashflow_details c
WHERE c.kategoria = 'Transfery'
    AND c.subkategoria IN ('{}')
GROUP BY date(c.data, 'Start of month')