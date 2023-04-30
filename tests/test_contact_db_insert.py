import unittest
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as chrome_service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from flask_testing import LiveServerTestCase
from urllib.request import urlopen
from app import app_factory
from src.route_handler.route_handler import config_routs
import sqlite3


class ContactsPage(LiveServerTestCase):
    driver: webdriver = webdriver.Chrome(
        service=chrome_service(ChromeDriverManager().install())
    )
    good_data: dict = {
        "first_name": "Evan",
        "last_name": "Rikker",
        "phone_number": "5551114444",
        "email": "Test@email.com",
        "subject": "Test",
        "message": "Pop Quiz",
    }

    def test_server_is_up_and_running(self) -> None:
        server_address = f"{self.get_server_url()}/ContactMe"
        response = urlopen(server_address)
        self.assertEqual(response.code, 200)

    def create_app(self) -> Flask:
        app_instance, database_instance = app_factory(True)
        app_instance.config["DEBUG"] = True
        app_instance.config["LIVESERVER_TIMEOUT"] = 10
        app_instance.config["LIVESERVER_PORT"] = 0
        config_routs(app_instance, database_instance)
        return app_instance

    def test_correct_data_input_passes(self) -> None:
        server_address: str = f"{self.get_server_url()}/ContactMe"
        self.driver.get(server_address)
        for key, value in self.good_data.items():
            element = self.driver.find_element(By.ID, key)
            element.send_keys(value)
        self.driver.find_element(By.ID, "submit").click()
        key_list = [
            "first_name",
        ]

        db = sqlite3.connect("test.db")
        direct_query = db.execute(
            "select first_name "
            "from leads where email = 'Test@email.com' and visible = 1"
        )
        test_result = dict(zip(key_list, direct_query.fetchall()))
        retrieved_data = test_result
        self.assertEqual("Evan", retrieved_data["first_name"][0])


if __name__ == "__main__":
    unittest.main()
