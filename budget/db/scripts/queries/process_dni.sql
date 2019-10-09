create table dni as
 WITH RECURSIVE dates(date) AS (
  VALUES(date('now'))
  UNION ALL
  SELECT date(date, '1 day')
  FROM dates
  limit 365*3
)
SELECT date [dzien] FROM dates;