CREATE TABLE monthly_budget_execution AS
SELECT m.miesiac, ifnull(xx.kategoria, 'BLANK') [kategoria], ifnull(xx.subkategoria, 'BLANK') [subkategoria],  ifnull(xx.kwota, 0) [kwota]
FROM miesiace m
LEFT OUTER JOIN (
    SELECT
        w.miesiac,
        w.kategoria,
        w.subkategoria,
        w.kwota
    from
        wydatki w
    UNION
    select
        w.miesiac,
        w.kategoria,
        w.subkategoria,
        w.kwota    
    from
        wplywy w
) xx ON date(xx.miesiac) = m.miesiac
ORDER BY m.miesiac, kategoria, subkategoria