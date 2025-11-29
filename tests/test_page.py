"""
This module contains tests for module page.

"""
import unittest
from src.page import Page

class TestPage(unittest.TestCase):
    def test_page_equality(self) -> None:
        """
        tests if two pages are equal
        """
        page1 = Page(route="home", title="Welcome", content="Welcome to our website!")
        page2 = Page(route="home", title="Welcome", content="Welcome to our website!")
        self.assertEqual(page1, page2)

    def test_page_inequality(self) -> None:
        """
        tests if two pages are not equal
        """
        page1 = Page(route="home", title="Welcome", content="Welcome to our website!")
        page2 = Page(route="services", title="Our Services", content="Here are our services.")
        self.assertNotEqual(page1, page2)
