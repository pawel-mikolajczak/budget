create table cashflow_details as
SELECT
    x.konto [konto],
    d.dzien [data],
    x.kategoria [kategoria],
    x.subkategoria [subkategoria],
    x.detale [detale],
    CAST(x.minimum AS REAL) [min],
    CAST(x.average AS REAL) [avg],
    CAST(x.maximum AS REAL) [max]
FROM dni d
    LEFT OUTER JOIN (
        SELECT
            konto,
            data,
            kategoria,
            subkategoria,
            detale,
            minimum,
            average,
            maximum
        FROM nieregularne
        WHERE final_paid_date = 'NaT'
        UNION ALL
        SELECT
            konto,
            final_paid_date AS data,
            kategoria,
            subkategoria,
            detale,
            finally_paid AS minimum,
            finally_paid AS average,
            finally_paid AS maximum
        FROM nieregularne
        WHERE final_paid_date <> 'NaT'
        UNION ALL
        SELECT
            konto,
            data,
            kategoria,
            subkategoria,
            detale,
            minimum,
            average,
            maximum
        FROM miesieczne
        UNION ALL
        SELECT
            'K - mBank' [konto],
            data,
            "Stan konta" [kategoria],
            "Stan konta" [subkategoria],
            "Stan konta" [detale],
            stan_konta [minimum],
            stan_konta [average],
            stan_konta [maximum]
         FROM mbank_stan_konta
    ) x
        ON date(x.data) = d.dzien
ORDER BY d.dzien ASC