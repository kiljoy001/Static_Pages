"""
Module for interacting with sql database.
"""
import sqlite3
import logging

DB_NAME_FILENAME = "data.db"
DB_TABLE_NAME = "leads"


class DatabaseOperation:
    """
    Class for setting up, changing, reading, updating or deleting data in sqlite db
    """

    def __init__(self, db_file_name: str = DB_NAME_FILENAME, sqlite_connection: sqlite3.Connection = None,
) -> None:
        if sqlite_connection:
            self.connection = sqlite_connection
        else:
            self.connection = sqlite3.connect(db_file_name)
        logging.basicConfig(
            filename="database.log", encoding="utf8", level=logging.DEBUG
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Close the database connection
        @return: null
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            logging.info("Database connection closed")

    def commit(self):
        """
        Commit changes to the database
        @return:
        """
        try:
            self.connection.commit()
            logging.info("Transaction commited")
        except sqlite3.IntegrityError as error:
            logging.error("Failed to commit transaction: %s", error)

    def rollback(self):
        """
        Roll back the changes to the database
        @return:
        """
        try:
            self.connection.rollback()
            logging.info("Transaction rolled back")
        except sqlite3.Error as error:
            logging.error("Failed to roll back transaction: %s", error)

    def create_leads_table(self, db_table_name: str) -> bool:
        """
        Creates a new table with the fields id, first name,
        last name, phone number, email, subject, message & visible
        @param db_table_name: name of the new table
        @return: bool
        """
        try:
            self.connection.execute(
                f"create table if not exists {db_table_name}("
                "id INTEGER PRIMARY KEY,"
                "first_name TEXT NOT NULL,"
                "last_name TEXT NOT NULL,"
                "phone_number TEXT NOT NULL,"
                "email TEXT UNIQUE NOT NULL,"
                "subject TEXT NOT NULL,"
                "message TEXT NOT NULL,"
                "visible INTEGER NOT NULL)"
            )
            self.connection.commit()
            logging.info("Database %s created.", db_table_name)
            logging.info("Database table %s was created", db_table_name)
            return True
        except sqlite3.Error as error:
            logging.error("Unable to create database %s. %s", DB_NAME_FILENAME, error)
            return False

    def insert_contact_data(self, data: dict) -> bool:
        """
        Inserts data into leads table
        @type data: dict
        """
        try:
            self.connection.execute(
                "INSERT INTO leads (first_name,"
                "last_name,"
                "phone_number,"
                "email,"
                "subject,"
                "message,"
                "visible)"
                "VALUES (:first_name, :last_name, :phone_number, :email, :subject, :message, :visible)",
                data,
            )
            self.connection.commit()
            logging.info("Data inserted into database")
            return True
        except sqlite3.Error as error:
            logging.error("Data insertion failed :(\n%s", error)
            return False

    def disable_contact(self, email: str) -> bool:
        """
        Hides data from the front end instead of a hard delete - updates visible field to false
        @param email: email address
        """
        try:
            self.connection.execute("UPDATE leads set visible=0 where email = ?", (email,))
            self.connection.commit()
            logging.info("Email address %s was disabled.", email)
            return True
        except sqlite3.Error as error:
            logging.error("%s was not disabled. Error: %s", email, error)
            return False

    def update_contact(self, data: dict, email: str) -> bool:
        """
        Updates contacts from leads database, updates all fields
        @param email: is the email address to look for to do the update op
        @param data: dict[str|int] Keys much match table columns
        @return: bool
        """
        try:
            params = {**data, "email_old": email}
            logging.debug("Parameters for update: %s", params)
            cursor = self.connection.execute(
                """
                UPDATE leads SET
                    first_name = :first_name,
                    last_name = :last_name,
                    phone_number = :phone_number,
                    email = :email,
                    subject = :subject,
                    message = :message,
                    visible = :visible
                WHERE email = :email_old
                """,
                params,
            )
            self.connection.commit()
            if cursor.rowcount == 0:
                logging.warning("No contact found with email: %s", email)
                return False
            logging.info("Contact %s has been updated.", data["email"])
            return True
        except sqlite3.IntegrityError as error:
            logging.error("%s was not updated Error: %s", data["email"], error)
            return False

    def get_contact(self, data: str) -> dict:
        """
        Returns contact by email address if marked visible
        @param data: email address
        @return:
        """
        d_keys = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "subject",
            "message",
        ]
        try:
            fetch = self.connection.execute(
                f"select first_name, last_name, phone_number, email, subject, message"
                f" from leads where visible = 1 and email = '{data}'"
            )
            returned_data = fetch.fetchone()
            formatted_dict = dict(zip(d_keys, returned_data))
            logging.info("Contact %s was found", data)
            return formatted_dict
        except sqlite3.Error as error:
            logging.error("%s was not found. Error: %s", data, error)
            return {}
