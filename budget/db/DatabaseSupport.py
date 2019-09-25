import sqlite3
import os


class DatabaseSupport:

    def __init__(self):
        self.sqliteConnection = None

    def initDatabase(self):
        try:
            dbfile = 'inmemorydatabase.db'
            if os.path.exists(dbfile):
                os.remove(dbfile)
            self.sqliteConnection = sqlite3.connect(dbfile)
            cursor = self.sqliteConnection.cursor()
            print("Database created and Successfully Connected to SQLite")

            sqlite_select_Query = "select sqlite_version();"
            cursor.execute(sqlite_select_Query)
            record = cursor.fetchall()
            print("SQLite Database Version is: ", record)
            cursor.close()

            self.create_table('wydatki.sql')

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def create_table(self, table_sql):
        cursor = self.sqliteConnection.cursor()
        with open('../budget/db/%s' % table_sql, 'r') as sqlite_file:
            sql_script = sqlite_file.read()
        cursor.executescript(sql_script)
        print("Table {} created".format(table_sql))
        cursor.close()

    def add_wydatek(self, miesiac, kategoria, subkategoria, kwota):
        cursor = self.sqliteConnection.cursor()

        sqlite_insert_query = "INSERT INTO wydatki ('miesiac', 'kategoria', 'subkategoria', 'kwota') VALUES ('{}','{}','{}',{})".format(miesiac, kategoria, subkategoria, kwota)

        count = cursor.execute(sqlite_insert_query)
        self.sqliteConnection.commit()
        print("Wydatek {}, {}, {}, {} added: {} rows".format(miesiac, kategoria, subkategoria, kwota, cursor.rowcount))
        cursor.close()

    def closeConnection(self):
        if (self.sqliteConnection):
            self.sqliteConnection.close()
            print("The SQLite connection is closed")
