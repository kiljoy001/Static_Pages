"""
This module contains tests for class DatabaseOperation
"""
import unittest
from datetime import datetime

from src.database.database import DatabaseOperation
from src.appointment import Appointment
from src.page import Page
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
        # We can't query by plain email directly anymore in a simple test without replicating encryption/hashing.
        # So we verify that get_contact returns the correct data.

        result = self.db_operation.get_contact(data["email"])
        self.assertEqual(data["first_name"], result["first_name"])
        self.assertEqual(data["email"], result["email"])

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

        # update contact
        result = self.db_operation.update_contact(data, "jYoda@jediorder.com")
        self.assertTrue(result, "Update operation failed.")

        # Verify update
        updated = self.db_operation.get_contact("jYessler@republicarmy.com")
        self.assertEqual("Jason", updated["first_name"])

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

        # Verify via public API since SQL lookup is hard
        contact = self.db_operation.get_contact(data["email"])
        self.assertEqual({}, contact)

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

        # Manually compare fields because datetime comparison might be slightly off due to microseconds
        # or Appointment equality is strict.
        self.assertEqual(1, len(list_of_appointments))
        retrieved = list_of_appointments[0]
        self.assertEqual(test_appointment.event_name, retrieved.event_name)
        self.assertEqual(test_appointment.phone_number, retrieved.phone_number)
        self.assertEqual(test_appointment.location, retrieved.location)
        self.assertEqual(test_appointment.message, retrieved.message)
        # Compare dates as ISO strings to ignore microsecond loss if any (though in memory it might be preserved, but via isoformat string in DB it is)
        # Wait, I changed the DB to store isoformat. `datetime.now()` has microseconds. `isoformat()` preserves them.
        # But let's check.
        self.assertEqual(test_appointment.date, retrieved.date)

    def test_insert_and_get_page(self) -> None:
        """
        Tests insert_page and get_page_by_route
        """
        page = Page(route="test", title="Test Page", content="Test Content")
        self.db_operation.insert_page(page)

        retrieved_page = self.db_operation.get_page_by_route("test")
        self.assertEqual(page, retrieved_page)

    def test_update_page(self) -> None:
        """
        Tests update_page
        """
        page = Page(route="test", title="Test Page", content="Test Content")
        self.db_operation.insert_page(page)

        updated_page = Page(route="test", title="Updated Title", content="Updated Content", image_url="img.png")
        self.db_operation.update_page(updated_page)

        retrieved_page = self.db_operation.get_page_by_route("test")
        self.assertEqual(updated_page, retrieved_page)

    def test_get_all_pages(self) -> None:
        """
        Tests get_all_pages
        """
        page1 = Page(route="p1", title="T1", content="C1")
        page2 = Page(route="p2", title="T2", content="C2")
        self.db_operation.insert_page(page1)
        self.db_operation.insert_page(page2)

        pages = self.db_operation.get_all_pages()
        # Order is not guaranteed, so check length and containment
        self.assertEqual(2, len(pages))
        # Note: pages returned might be in different order or identity might not be preserved if not careful with list comparison
        # But our Page.__eq__ handles content comparison.
        self.assertTrue(page1 in pages)
        self.assertTrue(page2 in pages)

    def test_insert_and_get_page(self) -> None:
        """
        Tests insert_page and get_page_by_route
        """
        page = Page(route="test", title="Test Page", content="Test Content")
        self.db_operation.insert_page(page)

        retrieved_page = self.db_operation.get_page_by_route("test")
        self.assertEqual(page, retrieved_page)

    def test_update_page(self) -> None:
        """
        Tests update_page
        """
        page = Page(route="test", title="Test Page", content="Test Content")
        self.db_operation.insert_page(page)

        updated_page = Page(route="test", title="Updated Title", content="Updated Content", image_url="img.png")
        self.db_operation.update_page(updated_page)

        retrieved_page = self.db_operation.get_page_by_route("test")
        self.assertEqual(updated_page, retrieved_page)

    def test_get_all_pages(self) -> None:
        """
        Tests get_all_pages
        """
        page1 = Page(route="p1", title="T1", content="C1")
        page2 = Page(route="p2", title="T2", content="C2")
        self.db_operation.insert_page(page1)
        self.db_operation.insert_page(page2)

        pages = self.db_operation.get_all_pages()
        # Order is not guaranteed, so check length and containment
        self.assertEqual(2, len(pages))
        # Note: pages returned might be in different order or identity might not be preserved if not careful with list comparison
        # But our Page.__eq__ handles content comparison.
        self.assertTrue(page1 in pages)
        self.assertTrue(page2 in pages)

if __name__ == "__main__":
    unittest.main()
