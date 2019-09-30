import sqlite3
import os
import logging

logger = logging.getLogger("DatabaseSupport")
logger.setLevel(logging.INFO)

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
            logger.debug("Database created and Successfully Connected to SQLite")

            sqlite_select_Query = "select sqlite_version();"
            cursor.execute(sqlite_select_Query)
            record = cursor.fetchall()
            logger.info("SQLite Database Version is: {}".format(record))
            cursor.close()

            self.create_table('wydatki.sql')
            self.create_table('wplywy.sql')
            self.create_table('konta.sql')
            self.create_table('nieregularne.sql')

        except sqlite3.Error as error:
            logger.error("Error while connecting to sqlite", error)

    def create_table(self, table_sql):
        cursor = self.sqliteConnection.cursor()
        with open('../budget/db/%s' % table_sql, 'r') as sqlite_file:
            sql_script = sqlite_file.read()
        cursor.executescript(sql_script)
        logger.info("Table {} created".format(table_sql))
        cursor.close()

    def select_data_via_script(self, script):
        cursor:sqlite3.Cursor = self.sqliteConnection.cursor()
        script_path = '../budget/db/%s' % script
        with open(script_path, 'r') as sqlite_file:
            sql_script = sqlite_file.read()
        cursor.execute(sql_script)
        records = cursor.fetchall()
        logger.info("Total rows for query '{}' are: {}".format(script_path, len(records)))
        cursor.close()
        return records

    def insert_data(self, query, type):
        logger.debug("INSERT Query '{}'".format(query))
        cursor = self.sqliteConnection.cursor()
        cursor.execute(query)
        self.sqliteConnection.commit()
        logger.debug("{} added: {} rows".format(type, cursor.rowcount))
        cursor.close()

    def select_data(self, query):
        logger.info("SELECT Query '{}'".format(query))
        cursor = self.sqliteConnection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        logger.info("Total rows for query '{}' are: {}".format(query, len(records)))
        cursor.close()
        return records

    def closeConnection(self):
        if (self.sqliteConnection):
            self.sqliteConnection.close()
            logger.debug("The SQLite connection is closed")
