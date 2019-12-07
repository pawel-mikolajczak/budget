SELECT date(x.data, 'Start of month') [data], SUM(x."min") [min], SUM(x."avg") [avg], SUM(x."max") [max]
FROM (
    SELECT date(c.data, 'Start of month') [data], c."min"*-1 [min], c."avg"*-1 [avg], c."max"*-1 [max]
    FROM cashflow_details c
    WHERE c.kategoria = 'Transfery'
        AND c.subkategoria IN ('{}')
    UNION ALL
    SELECT date(c.data, 'Start of month') [data], c."min" [min], c."avg" [avg], c."max" [max]
    FROM cashflow_details c
    WHERE c.konto = '{}'
) AS x
GROUP BY date(x.data, 'Start of month')