CREATE TABLE nieregularne (
 id INTEGER PRIMARY KEY,
 data datetime NOT NULL,
 kategoria text NOT NULL,
 subkategoria text NOT NULL,
 detale text NOT NULL,
 minimum real NOT NULL,
 average real NOT NULL,
 maximum real NOT NULL,
 finally_paid real NULL,
 final_paid_date datetime NULL,
 comments text NULL
);