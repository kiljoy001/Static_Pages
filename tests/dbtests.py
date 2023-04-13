import unittest
import database_mock


class MyTestCase(unittest.TestCase):

    def db_insert_returns_correct_data(self):

        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
