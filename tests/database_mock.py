"""
Creates an in-memory sqlite database to run tests on.
"""
import sqlite3
import sys
import logging
from unittest import TestCase

from src.database.database import DatabaseOperation

DB_NAME_FILENAME = ":memory:"
DB_TABLE_NAME = "leads"


class MockDatabase(TestCase):
    """
    tests Database connection methods to check if the right data is returned in the proper format
    """

    def setUp(self) -> None:
        self.connection = sqlite3.connect(DB_NAME_FILENAME)
        self.create_database()
        self.db_operation = DatabaseOperation(sqlite_connection=self.connection)

    def tearDown(self) -> None:
        self.connection.close()
        logging.info("Connection has been closed.")

    def create_database(self) -> None:
        # Create table
        self.connection.execute("DROP TABLE IF EXISTS leads")
        self.connection.execute(
            f"CREATE TABLE {DB_TABLE_NAME} ("
            "id INTEGER PRIMARY KEY,"
            "first_name TEXT NOT NULL,"
            "last_name TEXT NOT NULL,"
            "phone_number TEXT NOT NULL,"
            "email TEXT NOT NULL,"
            "email_hash TEXT UNIQUE,"
            "subject TEXT NOT NULL,"
            "message TEXT NOT NULL,"
            "visible INTEGER NOT NULL)"
        )
        self.connection.execute(
            "CREATE TABLE appointments ("
            "id INTEGER PRIMARY KEY,"
            "date TEXT NOT NULL,"
            "event_name TEXT NOT NULL,"
            "phone_number TEXT NOT NULL,"
            "location TEXT NOT NULL,"
            "message TEXT NOT NULL)"
        )
        self.connection.execute(
            "CREATE TABLE pages ("
            "id INTEGER PRIMARY KEY,"
            "route TEXT UNIQUE NOT NULL,"
            "title TEXT NOT NULL,"
            "content TEXT NOT NULL,"
            "image_url TEXT)"
        )
        self.connection.commit()
        logging.info(f"Database {DB_NAME_FILENAME} has been created.")
        logging.info(f"Database table {DB_TABLE_NAME} was created.")
