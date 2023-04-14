import unittest
from src.database.database import DatabaseOperation
from database_mock import MockDatabase
from unittest.mock import patch, MagicMock


class MyTestCase(MockDatabase):
    def setUp(self) -> None:
        self.dbop_object = DatabaseOperation()
    @patch('src.database.database.insert_contact')
    def test_insert_contact(self, insert_mock):
        # Arrange
        data = {
            'first_name': 'Jacob',
            'last_name': 'Yoda',
            'phone_number': '18005551111',
            'email': 'jYoda@jediorder.com',
            'subject': 'Secret',
            'message': 'Stolen holocron at Balmoora. Send the fleet. In persuit',
            'visible': 1
        }
        insert_mock = MagicMock()
        insert_mock.insert_contact.return_value = True
        insert_mock.return_value = insert_mock

        # Act
        result = self.dbop_object.insert_contact(data)
        expected = True
        self.assertEqual(result, expected)







if __name__ == '__main__':
    unittest.main()
