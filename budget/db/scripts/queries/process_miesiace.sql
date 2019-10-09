create table miesiace as
select distinct date(miesiac) [miesiac]
from
(
    select distinct miesiac
    from wydatki

    union

    select distinct miesiac
    from wplywy

    union

    select distinct date(data, 'Start of month') [miesiac]
    from konta
) x
order by 1 desc