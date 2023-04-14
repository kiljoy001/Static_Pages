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
                    "message TEXT NOT NULL,"
                    "visible INTEGER NOT NULL)"
                )
                self.connection.commit()
                logging.info('Database table leads was created')
            except sqlite3.Error as error:
                if error.sqlite_errorcode == sqlite3.ProgrammingError:
                    logging.error('Table leads already exists')
                else:
                    logging.error(f"Error detected:\n{error}")

    def insert_contact(self, **data) -> bool:
        """
        Inserts data into leads table
        """
        try:
            for iterator, (key, value) in enumerate(data.items()):
                self.connection.execute(f"insert into leads ({key}) values (?)", value)
            self.connection.commit()
            logging.info("Data inserted into database")
            return True
        except sqlite3.Error as error:
            logging.error(f"Data insertion failed :( \n {error}")
            self.connection.close()
            return False

    def remove_contact(self):
        """
        Hides data from the front end instead of a hard delete - updates visible field to false
        """
        pass

    def update_contact(self, data: dict):
        """
        Updates fields from
        @param data:
        @return:
        """
        pass
