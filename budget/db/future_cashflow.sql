SELECT
    data [data],
    detale [detale],
    minimum [min],
    average [avg],
    maximum [max]
FROM nieregularne
WHERE final_paid_date = 'NaT'
ORDER BY data ASC