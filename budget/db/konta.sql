CREATE TABLE konta (
 id INTEGER PRIMARY KEY,
 konto text NOT NULL,
 data datetime NOT NULL,
 opis text NOT NULL,
 kwota NUMERIC(10,2) NOT NULL,
 bilans NUMERIC(10,2) NOT NULL
);