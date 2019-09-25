CREATE TABLE wydatki (
 id INTEGER PRIMARY KEY,
 miesiac datetime NOT NULL,
 kategoria text NOT NULL,
 subkategoria text NOT NULL,
 kwota NUMERIC(10,2) NOT NULL
);