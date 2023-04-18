"""
Creates an in-memory sqlite database to run tests on.
"""
import sqlite3
import sys
from unittest import TestCase

DB_NAME_FILENAME = ":memory:"
DB_TABLE_NAME = "leads"


class MockDatabase(TestCase):
    """
    tests Database connection methods to check if the right data is returned in the proper format
    """

    connection = sqlite3.connect(DB_NAME_FILENAME)

    @classmethod
    def setUpClass(cls) -> None:
        cls.connection = sqlite3.connect(DB_NAME_FILENAME)
        test_form_data = {
            "first_name": "John",
            "last_name": "Smith",
            "phone_number": "15554567",
            "email": "test@testdomain.com",
            "subject": "Testing this out!",
            "message": "This is a test message, please ignore!",
            "visible": 1,
        }
        if cls.connection:
            # try to create database
            try:
                cls.connection.execute(
                    f"create table if not exists {DB_TABLE_NAME}("
                    "id INTEGER PRIMARY KEY,"
                    "first_name TEXT NOT NULL,"
                    "last_name TEXT NOT NULL,"
                    "phone_number TEXT NOT NULL,"
                    "email TEXT NOT NULL,"
                    "subject TEXT NOT NULL,"
                    "message TEXT NOT NULL,"
                    "visible INTEGER NOT NULL)"
                )
                cls.connection.commit()
                print(f"Database {DB_NAME_FILENAME} created.")
                print(f"Database table {DB_TABLE_NAME} was created")
            except sqlite3.Error as error:
                print(f"Unable to create database {DB_NAME_FILENAME}.\n{error}")
                sys.exit(1)

        # Insert into database0
        try:
            cls.connection.execute(
                "INSERT INTO leads (first_name, last_name, phone_number, email, subject, message, "
                "visible)"
                "VALUES (:first_name, :last_name, :phone_number,:email, :subject, :message, "
                ":visible)",
                test_form_data,
            )
            cls.connection.commit()
            print(f"Insertion into {DB_TABLE_NAME} succeeded")
        except sqlite3.Error as error:
            print(f"Data insertion failed :(\n{error}")
            cls.connection.close()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.connection = sqlite3.connect(DB_TABLE_NAME)
        # drop the database if it already exists
        try:
            cls.connection.close()
            print("Database dropped!")
        except sqlite3.Error as error:
            print(
                f"{DB_TABLE_NAME} Had an error dropping database. Error as follows:\n{error}"
            )
        finally:
            cls.connection.close()
