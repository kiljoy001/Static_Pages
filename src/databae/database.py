import sqlite3
import logging

DB_NAME = "leads.db"


class DatabaseOperation:
    """
    Class for setting up, changing, reading, updating or deleting data in sqlite db
    """

    def __init__(self):
        self.connection = sqlite3.connect(DB_NAME)
        logging.basicConfig(filename='database.log', encoding='utf8', level=logging.DEBUG)
        if self.connection:
            # try to create database
            try:
                self.connection.execute(f"create database {DB_NAME} default character set 'utf8'")
                logging.info(f"Database {DB_NAME} created.")
            except sqlite3.Error as error:
                logging.error(f"Unable to create database {DB_NAME}.\n{error}")
                exit(1)
            # try making tables
            try:
                self.connection.execute(
                    "create table leads("
                    "id INTEGER PRIMARY KEY,"
                    "first_name TEXT NOT NULL,"
                    "last_name TEXT NOT NULL,"
                    "phone_number TEXT NOT NULL,"
                    "email TEXT NOT NULL,"
                    "subject TEXT NOT NULL,"
                    "message TEXT NOT NULL )"
                )
                self.connection.commit()
                logging.info('Database table leads was created')
            except sqlite3.Error as error:
                if error.sqlite_errorcode == sqlite3.ProgrammingError:
                    logging.error('Table leads already exists')
                else:
                    logging.error(f"Error detected:\n{error}")
