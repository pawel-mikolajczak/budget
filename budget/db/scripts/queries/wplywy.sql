CREATE TABLE wplywy AS
SELECT x.miesiac as miesiac, x.kategoria as kategoria, x.subkategoria as subkategoria, CAST(SUM(CAST(kwota AS REAL)) AS REAL) AS kwota
FROM (
    SELECT date(miesiac, 'Start of month') [miesiac], kategoria, subkategoria, kwota
    FROM wplywy_mbank
    UNION ALL
    SELECT date(k.data, 'Start of month') [miesiac], kategoria, podkategoria [subkategoria], kwota [kwota]
    FROM konta k
    WHERE k.kategoria = '{}'
) AS x
group by x.miesiac, x.kategoria, x.subkategoria