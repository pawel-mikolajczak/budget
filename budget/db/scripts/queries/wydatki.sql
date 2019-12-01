CREATE TABLE wydatki as
SELECT miesiac [miesiac], kategoria, subkategoria, CAST(SUM(kwota) AS REAL)  [kwota]
FROM (
    SELECT date(miesiac, 'Start of month') [miesiac], kategoria, subkategoria, kwota
    FROM wydatki_mbank
    UNION ALL
    SELECT date(k.data, 'Start of month') [miesiac], kategoria, podkategoria [subkategoria], kwota*-1 [kwota]
    FROM konta k
    WHERE k.kategoria not in ('Admin', 'Transfery', 'Wpływy')
)
group by miesiac, kategoria, subkategoria