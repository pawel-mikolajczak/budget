SELECT
    d.dzien [data],
    x.kategoria [kategoria],
    x.subkategoria [subkategoria],
    x.detale [detale],
    x.minimum [min],
    x.average [avg],
    x.maximum [max]
FROM dni d
    LEFT OUTER JOIN (
        SELECT
            data,
            kategoria,
            subkategoria,
            detale,
            minimum,
            average,
            maximum
        FROM nieregularne
        WHERE final_paid_date = 'NaT'
        UNION
        SELECT
            data,
            kategoria,
            subkategoria,
            detale,
            minimum,
            average,
            maximum
        FROM miesieczne
    ) x
        ON date(x.data) = d.dzien
ORDER BY d.dzien ASC