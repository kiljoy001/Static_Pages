"""
This module contains tests for class DatabaseOperation
"""
import unittest
from src.database.database import DatabaseOperation
import tests.database_mock


class MyTestCase(tests.database_mock.MockDatabase):
    """
    Database Test Class
    """

    def setUp(self) -> None:
        self.dbop_object = DatabaseOperation("memory")

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
        result = self.dbop_object.insert_data(data, "leads")
        expected = True
        # Assert
        self.assertEqual(result, expected)

    def test_get_contact(self) -> None:
        """
        Tests disable contact method
        @return:
        """
        data = {"email": "jYoda@jediorder.com"}
        direct_query = self.connection.execute(
            "select email from leads where email = 'jYoda@jediorder.com' and visible = 1"
        )

        # Compare results
        self.assertEqual(self.dbop_object.get_contact(data), direct_query)

    def test_update_contact(self) -> None:
        """
        Tests the ability to update contact information
        @return:
        """
        data = {"email": "jYoda@republicarmy.com"}
        self.dbop_object.update_contact(data, "leads")
        direct_query = self.connection.execute(
            "select first_name from leads where email = 'jYoda@republicarmy.com'"
        )
        self.assertEqual("Jacob", direct_query)


if __name__ == "__main__":
    unittest.main()
