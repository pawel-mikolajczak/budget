SELECT date(miesiac, 'Start of month') [miesiac], kategoria, subkategoria, SUM(kwota) [kwota]
FROM (
    SELECT date(miesiac, 'Start of month') [miesiac], kategoria, subkategoria, kwota
    FROM wydatki
    UNION ALL
    SELECT date(k.data, 'Start of month') [miesiac], kategoria, podkategoria [subkategoria], kwota*-1 [kwota]
    FROM konta k
    WHERE k.kategoria not in ('Admin', 'Transfery', 'Wpływy')
)
group by miesiac, kategoria, subkategoria