"""
Module for interacting with sql database.
"""
import sqlite3
import logging
import sys

DB_NAME_FILENAME = "data.db"
DB_TABLE_NAME = "leads"


class DatabaseOperation:
    """
    Class for setting up, changing, reading, updating or deleting data in sqlite db
    """

    def __init__(
        self,
        db_file_name: str = DB_NAME_FILENAME,
        db_table_name: str = DB_TABLE_NAME,
        sqlite_connection: sqlite3.Connection = None,
    ):
        self.sqlite_connection = sqlite_connection
        if self.sqlite_connection:
            self.connection = self.sqlite_connection
        else:
            self.connection = sqlite3.connect(db_file_name)
        logging.basicConfig(
            filename="database.log", encoding="utf8", level=logging.DEBUG
        )
        if self.connection:
            # try to create database
            try:
                self.connection.execute(
                    f"create table if not exists {db_table_name}("
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
                logging.info("Database %s created.", db_table_name)
                logging.info("Database table %s was created", db_table_name)
            except sqlite3.Error as error:
                logging.error("Unable to create database %s. %s", db_file_name, error)
                sys.exit(1)

    def insert_data(self, data: dict, db_table_name: str = DB_TABLE_NAME) -> bool:
        """
        Inserts data into leads table
        """
        try:
            for key, value in data.items():
                self.connection.execute(
                    f"insert into {db_table_name} ({key}) values (?)", (value,)
                )
                self.connection.commit()
            logging.info("Data inserted into database")
            return True
        except sqlite3.Error as error:
            logging.error("Data insertion failed :(\n%s", error)
            self.connection.close()
            return False

    def disable_contact(self, data: dict, db_table_name: str = DB_TABLE_NAME) -> bool:
        """
        Hides data from the front end instead of a hard delete - updates visible field to false
        @param data:
        @param db_table_name:
        """

    def update_contact(self, data: dict, db_table_name: str = DB_TABLE_NAME) -> bool:
        """
        Updates contacts from leads database
        @param db_table_name:
        @param data:
        @return:
        """

    def get_contact(self, data: dict, db_table_name: str = DB_TABLE_NAME):
        """
        @param data:
        @param db_table_name:
        @return:
        """
