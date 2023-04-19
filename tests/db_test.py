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
        result = DatabaseOperation(":memory:", self.connection).insert_contact_data(
            data
        )
        expected = True
        # Assert
        self.assertEqual(result, expected)

    def test_get_contact(self) -> None:
        """
        Tests get contact method
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
        data = "test@testdomain.com"
        direct_query = self.connection.execute(
            "select first_name, last_name, phone_number, email, subject, message "
            "from leads where email = 'test@testdomain.com' and visible = 1"
        )
        test_result = dict(zip(d_keys, direct_query.fetchall()))

        # Compare results
        self.assertEqual(
            test_result,
            DatabaseOperation(":memory:", self.connection).get_contact(data),
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
        DatabaseOperation(":memory:", self.connection).update_contact(data)
        direct_query = self.connection.execute(
            "select first_name from leads where email = 'jYessler@republicarmy.com'"
        )
        test_result = direct_query.fetchall()
        self.assertEqual("Jason", test_result[0][0])

    def test_disable_contact(self) -> None:
        """
        Tests if row is marked disabled in database
        @return:
        """
        data = "test@testdomain.com"
        DatabaseOperation(":memory:", self.connection).disable_contact(data)
        check = self.connection.execute(
            "select visible from leads where email = 'test@testdomain.com'"
        )
        test_result = check.fetchall()
        self.assertEqual(0, test_result[0][0])


if __name__ == "__main__":
    unittest.main()
