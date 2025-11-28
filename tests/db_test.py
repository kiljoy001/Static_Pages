"""
This module contains tests for class DatabaseOperation
"""
import unittest
from datetime import datetime

from src.database.database import DatabaseOperation
from src.appointment import Appointment
import tests.database_mock

class MyTestCase(tests.database_mock.MockDatabase):
    """
    Database Test Class
    """

    def test_insert_data(self):
        """
        Tests insert_data method
        @return:
        """
        # Arrange
        data = {
            "first_name": "Jacob",
            "last_name": "Yoda",
            "phone_number": "18005551111",
            "email": "jYoda@jediorder.com",
            "subject": "Secret",
            "message": "Stolen holocron at Balmoora. Send the fleet. In persuit",
            "visible": 1,
        }
        # Act

        result = self.db_operation.insert_contact_data(data)
        self.assertTrue(result)

    def test_get_contact(self) -> None:
        """
        Tests get contact method
        @return:
        """
        key_list = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "subject",
            "message",
        ]
        data = {
            "first_name": "John",
            "last_name": "Smith",
            "phone_number": "15554567",
            "email": "test@testdomain.com",
            "subject": "Testing this out!",
            "message": "This is a test message, please ignore!",
            "visible": 1,
        }

        self.db_operation.insert_contact_data(data)
        direct_query = self.connection.execute(
        "select first_name, last_name, phone_number, email, subject, message "
        "from leads where email = ? and visible = 1", (data["email"],)
        )
        row = direct_query.fetchone()
        test_result = dict(zip(key_list, row))
        # Compare results
        self.assertEqual(
            test_result,
            self.db_operation.get_contact(data["email"]),
        )

    def test_update_contact(self) -> None:
        """
        Tests the ability to update contact information
        @return:
        """
        data = {
            "first_name": "Jason",
            "last_name": "Yesler",
            "phone_number": "18005551111",
            "email": "jYessler@republicarmy.com",
            "subject": "Padawan Training Incomplete",
            "message": "Young Padawan, You have been deemed "
            "unfit to become a knight and will be removed from the order. "
            "You will be sent to the republic army instead.",
            "visible": 1,
        }

        original_data = {
            "first_name": "Jacob",
            "last_name": "Yoda",
            "phone_number": "18005551111",
            "email": "jYoda@jediorder.com",
            "subject": "Secret",
            "message": "Beware the dark side of the test.",
            "visible": 1,
            }
        self.db_operation.insert_contact_data(original_data)
        # verify original data
        cursor = self.connection.execute(
            "select * from leads where email = ? and visible = 1", (original_data["email"],)
        )
        original_entry = cursor.fetchone()
        self.assertIsNotNone(original_entry, "Original contact data is not found")

        # update contact
        result = self.db_operation.update_contact(data, "jYoda@jediorder.com")
        self.assertTrue(result, "Update operation failed.")

        direct_query = self.connection.execute(
            "select first_name from leads where email = ?", ("jYessler@republicarmy.com",)
            )
        test_result = direct_query.fetchone()
        self.assertEqual("Jason", test_result[0])

    def test_disable_contact(self) -> None:
        """
        Tests if row is marked disabled in database
        @return:
        """
        data = {
            "first_name": "John",
            "last_name": "Smith",
            "phone_number": "15554567",
            "email": "test@testdomain.com",
            "subject": "Testing this out!",
            "message": "This is a test message, please ignore!",
            "visible": 1,
        }
        self.db_operation.insert_contact_data(data)
        self.db_operation.disable_contact(data["email"])
        check = self.connection.execute(
            "select visible from leads where email = ?", ("test@testdomain.com",)
        )
        test_result = check.fetchone()
        self.assertEqual(0, test_result[0])

    def test_insert_duplicate_email_fails(self) -> None:
        """
        Test if the insert method returns an exception if a duplicate is attempted
        @return:
        """
        data = {
            "first_name": "Cin",
            "last_name": "Arolbun",
            "phone_number": "18005551111",
            "email": "cBun@imperialsecuritybureau.com",
            "subject": "Green Bisect",
            "message": "Jedi spotted at Markeb, please advise.",
            "visible": 1,
        }

        self.db_operation.insert_contact_data(data)
        op_result = self.db_operation.insert_contact_data(data)

        self.assertEqual(False, op_result)

    def test_role_type_has_correct_permission(self) -> None:
        """
        Test if the role has the correct type of permission
        @return:
        """
        roles = {
            "Administrator": "Administrator",
            "Editor": "Editor",
            "Appointment Setter": "Appointment",

        }

    def test_appointment_saved_to_database(self) -> None:
        """
        Tests if appointment has been saved to database
        @return:
        """
        # Arrange
        date = datetime.now()
        event_name = "Test Contact"
        phone_number = "+155555555"
        location = "Location 1"
        lead_message = "Interested in your services"

        # Act
        test_appointment = Appointment(date, event_name, phone_number, location, lead_message)
        self.db_operation.insert_appointment(test_appointment)

        #Assert
        list_of_appointments = self.db_operation.get_appointments(date)
        assert list_of_appointments == [test_appointment]

if __name__ == "__main__":
    unittest.main()
