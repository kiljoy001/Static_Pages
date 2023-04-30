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

    def __init__(
        self,
        db_file_name: str = DB_NAME_FILENAME,
        sqlite_connection: sqlite3.Connection = None,
    ) -> None:
        if sqlite_connection:
            self.connection = sqlite_connection
        else:
            self.connection = sqlite3.connect(db_file_name, check_same_thread=False)
        logging.basicConfig(
            filename="database.log", encoding="utf8", level=logging.DEBUG
        )
        self.create_leads_table("leads")

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

    def disable_contact(self, data: str) -> bool:
        """
        Hides data from the front end instead of a hard delete - updates visible field to false
        @param data: email address
        """
        try:
            self.connection.execute(f"UPDATE leads set visible=0 where email='{data}'")
            self.connection.commit()
            logging.info("Email address %s was disabled.", data)
            return True
        except sqlite3.Error as error:
            logging.error("%s was not disabled. Error: %s", data, error)
            return False

    def update_contact(self, data: dict, match: str) -> bool:
        """
        Updates contacts from leads database, updates all fields
        @param match: is the email address to look for to do the update op
        @param data: dict[str|int] Keys much match table columns
        @return: bool
        """
        try:
            email_address = match
            self.connection.execute(
                f"update leads set (first_name, last_name, phone_number, email, subject, message, "
                f"visible) = (:first_name, :last_name, :phone_number, :email, :subject, :message, "
                f":visible) where email = '{email_address}'",
                data,
            )
            self.connection.commit()
            logging.info("Contact %s has been updated.", data["email"])
            return True
        except sqlite3.Error as error:
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
            returned_data = fetch.fetchall()
            formatted_dict = dict(zip(d_keys, returned_data))
            logging.info("Contact %s was found", data)
            return formatted_dict
        except sqlite3.Error as error:
            logging.error("%s was not found. Error: %s", data, error)
            return {}
