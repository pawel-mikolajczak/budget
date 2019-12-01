CREATE TABLE miesieczne (
 id INTEGER PRIMARY KEY,
 data datetime NOT NULL,
 kategoria text NOT NULL,
 subkategoria text NOT NULL,
 detale text NOT NULL,
 minimum real NOT NULL,
 average real NOT NULL,
 maximum real NOT NULL
);