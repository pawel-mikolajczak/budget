CREATE TABLE nieregularne (
 id INTEGER PRIMARY KEY,
 data datetime NOT NULL,
 kategoria text NOT NULL,
 subkategoria text NOT NULL,
 detale text NOT NULL,
 minimum NUMERIC(10,2) NOT NULL,
 average NUMERIC(10,2) NOT NULL,
 maximum NUMERIC(10,2) NOT NULL,
 finally_paid NUMERIC(10,2) NULL,
 final_paid_date datetime NULL,
 comment text NULL
);