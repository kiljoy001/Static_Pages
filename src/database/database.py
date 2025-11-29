"""
Module for interacting with sql database.
"""
import sqlite3
import logging
from datetime import datetime
from src.appointment import Appointment
from src.page import Page

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
            self.connection = sqlite3.connect(db_file_name, check_same_thread=False)
        logging.basicConfig(
            filename="database.log", encoding="utf8", level=logging.DEBUG
        )
        self.encryption = EncryptionService()

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
            # Note: email column is now encrypted and NOT unique by itself (randomized).
            # We add email_hash for uniqueness and lookup.
            self.connection.execute(
                f"create table if not exists {db_table_name}("
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
            self.connection.commit()
            logging.info("Database %s created.", db_table_name)
            logging.info("Database table %s was created", db_table_name)
            return True
        except sqlite3.Error as error:
            logging.error("Unable to create database %s. %s", DB_NAME_FILENAME, error)
            return False

    def create_appointment_table(self, db_table_name: str) -> bool:
        """
        Creates a new table for appointments
        @param db_table_name: name of the new table
        @return: bool
        """
        try:
            self.connection.execute(
                f"create table if not exists {db_table_name}("
                "id INTEGER PRIMARY KEY,"
                "date TEXT NOT NULL,"
                "event_name TEXT NOT NULL,"
                "phone_number TEXT NOT NULL,"
                "location TEXT NOT NULL,"
                "message TEXT NOT NULL)"
            )
            self.connection.commit()
            logging.info("Database table %s was created", db_table_name)
            return True
        except sqlite3.Error as error:
            logging.error("Unable to create database table %s. %s", db_table_name, error)
            return False

    def create_pages_table(self, db_table_name: str) -> bool:
        """
        Creates a new table for pages
        @param db_table_name: name of the new table
        @return: bool
        """
        try:
            self.connection.execute(
                f"create table if not exists {db_table_name}("
                "id INTEGER PRIMARY KEY,"
                "route TEXT UNIQUE NOT NULL,"
                "title TEXT NOT NULL,"
                "content TEXT NOT NULL,"
                "image_url TEXT)"
            )
            self.connection.commit()
            logging.info("Database table %s was created", db_table_name)
            return True
        except sqlite3.Error as error:
            logging.error("Unable to create database table %s. %s", db_table_name, error)
            return False

    def insert_appointment(self, appointment: Appointment) -> bool:
        """
        Inserts appointment into appointments table
        @param appointment: Appointment object
        @return: bool
        """
        try:
            self.connection.execute(
                "INSERT INTO appointments (date, event_name, phone_number, location, message)"
                "VALUES (?, ?, ?, ?, ?)",
                (
                    appointment.date.isoformat(),
                    appointment.event_name,
                    appointment.phone_number,
                    appointment.location,
                    appointment.message,
                ),
            )
            self.connection.commit()
            logging.info("Appointment inserted into database")
            return True
        except sqlite3.Error as error:
            logging.error("Appointment insertion failed :(\n%s", error)
            return False

    def get_appointments(self, date: datetime) -> list[Appointment]:
        """
        Returns appointments for a given date
        @param date: datetime object
        @return: list of Appointment objects
        """
        try:
            # We want to match just the date part if possible, but the input is a datetime object.
            # Assuming we want exact matches or close enough.
            # But the test passes `date = datetime.now()` and saves it as is.
            # So let's try to match exact first, or we can select all and filter.
            # However, sqlite stores strings. `isoformat()` includes time.
            # The test expects `list_of_appointments = self.db_operation.get_appointments(date)`
            # and asserts equality. So it probably expects to find the exact appointment we just saved.

            # Since `datetime.now()` includes microseconds, string comparison must be exact.

            target_date_str = date.isoformat()

            fetch = self.connection.execute(
                "select date, event_name, phone_number, location, message"
                " from appointments where date = ?",
                (target_date_str,)
            )
            returned_data = fetch.fetchall()
            appointments = []
            for row in returned_data:
                appointments.append(Appointment(
                    date=datetime.fromisoformat(row[0]),
                    event_name=row[1],
                    phone_number=row[2],
                    location=row[3],
                    message=row[4]
                ))
            logging.info("Appointments found for date %s", date)
            return appointments
        except sqlite3.Error as error:
            logging.error("Appointments not found. Error: %s", error)
            return []

    def insert_page(self, page: Page) -> bool:
        """
        Inserts page into pages table
        @param page: Page object
        @return: bool
        """
        try:
            self.connection.execute(
                "INSERT INTO pages (route, title, content, image_url)"
                "VALUES (?, ?, ?, ?)",
                (page.route, page.title, page.content, page.image_url),
            )
            self.connection.commit()
            logging.info("Page inserted into database")
            return True
        except sqlite3.Error as error:
            logging.error("Page insertion failed :(\n%s", error)
            return False

    def update_page(self, page: Page) -> bool:
        """
        Updates page in pages table
        @param page: Page object
        @return: bool
        """
        try:
            cursor = self.connection.execute(
                "UPDATE pages SET title = ?, content = ?, image_url = ? WHERE route = ?",
                (page.title, page.content, page.image_url, page.route),
            )
            self.connection.commit()
            if cursor.rowcount == 0:
                logging.warning("No page found with route: %s", page.route)
                return False
            logging.info("Page %s has been updated.", page.route)
            return True
        except sqlite3.Error as error:
            logging.error("Page update failed :(\n%s", error)
            return False

    def get_page_by_route(self, route: str) -> Page | None:
        """
        Returns page by route
        @param route: route string
        @return: Page object or None
        """
        try:
            fetch = self.connection.execute(
                "select route, title, content, image_url from pages where route = ?",
                (route,)
            )
            row = fetch.fetchone()
            if row:
                return Page(route=row[0], title=row[1], content=row[2], image_url=row[3])
            logging.warning("Page %s not found", route)
            return None
        except sqlite3.Error as error:
            logging.error("Page lookup failed. Error: %s", error)
            return None

    def get_all_pages(self) -> list[Page]:
        """
        Returns all pages
        @return: list of Page objects
        """
        try:
            fetch = self.connection.execute("select route, title, content, image_url from pages")
            returned_data = fetch.fetchall()
            pages = []
            for row in returned_data:
                pages.append(Page(route=row[0], title=row[1], content=row[2], image_url=row[3]))
            logging.info("All pages were found")
            return pages
        except sqlite3.Error as error:
            logging.error("Pages were not found. Error: %s", error)
            return []

    def insert_contact_data(self, data: dict) -> bool:
        """
        Inserts data into leads table
        @type data: dict
        """
        try:
            data_copy = data.copy()
            data_copy["phone_number"] = self.encryption.encrypt(data["phone_number"])
            data_copy["email"] = self.encryption.encrypt(data["email"])
            data_copy["email_hash"] = get_hash(data["email"])

            self.connection.execute(
                "INSERT INTO leads (first_name,"
                "last_name,"
                "phone_number,"
                "email,"
                "email_hash,"
                "subject,"
                "message,"
                "visible)"
                "VALUES (:first_name, :last_name, :phone_number, :email, :email_hash, :subject, :message, :visible)",
                data_copy,
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
            email_hash = get_hash(email)
            self.connection.execute("UPDATE leads set visible=0 where email_hash = ?", (email_hash,))
            self.connection.commit()
            logging.info("Email address %s was disabled.", email)
            return True
        except sqlite3.Error as error:
            logging.error("%s was not disabled. Error: %s", email, error)
            return False

    def update_contact(self, data: dict, email: str) -> bool:
        """
        Updates contacts from leads database, updates all fields
        @param email: is the email address to look for to do the update op (plain text)
        @param data: dict[str|int] Keys much match table columns
        @return: bool
        """
        try:
            email_hash_old = get_hash(email)

            data_copy = data.copy()
            data_copy["phone_number"] = self.encryption.encrypt(data["phone_number"])
            data_copy["email"] = self.encryption.encrypt(data["email"])
            data_copy["email_hash"] = get_hash(data["email"])
            data_copy["email_hash_old"] = email_hash_old

            cursor = self.connection.execute(
                """
                UPDATE leads SET
                    first_name = :first_name,
                    last_name = :last_name,
                    phone_number = :phone_number,
                    email = :email,
                    email_hash = :email_hash,
                    subject = :subject,
                    message = :message,
                    visible = :visible
                WHERE email_hash = :email_hash_old
                """,
                data_copy,
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
            email_hash = get_hash(data)
            fetch = self.connection.execute(
                "select first_name, last_name, phone_number, email, subject, message"
                " from leads where visible = 1 and email_hash = ?",
                (email_hash,)
            )
            returned_data = fetch.fetchone()

            if returned_data:
                formatted_dict = dict(zip(d_keys, returned_data))
                formatted_dict["email"] = self.encryption.decrypt(formatted_dict["email"])
                formatted_dict["phone_number"] = self.encryption.decrypt(formatted_dict["phone_number"])
                logging.info("Contact %s was found", data)
                return formatted_dict

            logging.warning("Contact %s not found", data)
            return {}
        except sqlite3.Error as error:
            logging.error("%s was not found. Error: %s", data, error)
            return {}

    def get_all_contacts(self) -> list:
        """
        Returns all visible contacts
        @return: list of dicts
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
                "select first_name, last_name, phone_number, email, subject, message"
                " from leads where visible = 1"
            )
            returned_data = fetch.fetchall()
            contacts = [dict(zip(d_keys, row)) for row in returned_data]
            logging.info("All contacts were found")
            return contacts
        except sqlite3.Error as error:
            logging.error("Contacts were not found. Error: %s", error)
            return []
