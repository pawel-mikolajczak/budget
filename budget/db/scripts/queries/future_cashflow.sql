SELECT
    d.dzien [data],
    n.detale [detale],
    n.minimum [min],
    n.average [avg],
    n.maximum [max]
FROM dni d
    LEFT OUTER JOIN nieregularne n
        ON date(n.data) = d.dzien
        AND n.final_paid_date = 'NaT'
ORDER BY d.dzien ASC