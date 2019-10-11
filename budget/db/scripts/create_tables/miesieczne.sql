CREATE TABLE miesieczne (
 id INTEGER PRIMARY KEY,
 data datetime NOT NULL,
 kategoria text NOT NULL,
 subkategoria text NOT NULL,
 detale text NOT NULL,
 minimum NUMERIC(10,2) NOT NULL,
 average NUMERIC(10,2) NOT NULL,
 maximum NUMERIC(10,2) NOT NULL
);