import unittest
import sqlite3

DB_NAME = "test.db"


class MockDatabase(unittest.TestCase):
    """
    tests Database connection methods to check if the right data is returned in the proper format
    """

    @classmethod
    def setUpClass(cls) -> None:
        connection = sqlite3.connect(DB_NAME)

        # drop the database if it already exists
        try:
            connection.execute(f"DROP DATABASE {DB_NAME}")
            connection.close()
            print("Database dropped!")
        except sqlite3.Error as error:
            print(f"{DB_NAME} {error}")

        test_form_data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'phone_number': '15554567',
            'email': 'test@testdomain.com',
            'subject': 'Testing this out!',
            'message': 'This is a test message, please ignore!'
        }
        # Create database
        try:
            connection.execute(
                f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'"
            )
        except sqlite3.Error as error:
            print(f"Failed creating database: {error}")
            exit(1)
        # Make tables
        try:
            connection.execute("create table leads("
                               "id INTEGER PRIMARY KEY,"
                               "first_name TEXT NOT NULL,"
                               "last_name TEXT NOT NULL,"
                               "phone_number TEXT NOT NULL,"
                               "email TEXT NOT NULL,"
                               "subject TEXT NOT NULL,"
                               "message TEXT NOT NULL )")
            connection.commit()
        except sqlite3.Error as error:
            if error.sqlite_errorcode == sqlite3.ProgrammingError:
                print("Table leads already exists.")
            else:
                print(error)
        else:
            print('OK, table created.')
        # Insert into database
        for iterator, (key, value) in enumerate(test_form_data.items()):
            connection.execute(f"insert into leads ({key}) values (?)", value)

    def tearDownClass(cls) -> None:
        connection = sqlite3.connect(DB_NAME)
        # drop the database if it already exists
        try:
            connection.execute(f"DROP DATABASE {DB_NAME}")
            connection.commit()
            print("Database dropped!")
            connection.close()
        except sqlite3.Error as error:
            print(f"{DB_NAME} Had and error dropping database. Error as follows: \n {error}")
        finally:
            connection.close()
