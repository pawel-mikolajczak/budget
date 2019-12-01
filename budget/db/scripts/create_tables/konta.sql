CREATE TABLE konta (
 id INTEGER PRIMARY KEY,
 konto text NOT NULL,
 data datetime NOT NULL,
 opis text NOT NULL,
 kwota real NOT NULL,
 bilans real NOT NULL,
 kategoria text NOT NULL,
 podkategoria text NOT NULL
);