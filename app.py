"""
This module is the main web app loop. Contains the app factory.
"""
from flask import Flask
from src.database.database import DatabaseOperation
from src.route_handler.route_handler import config_routes


def app_factory(testing=False):
    """
    Allows for application configuration for testing or production
    @return: Flask object
    """
    web_app = Flask(__name__)
    if testing:
        database = DatabaseOperation("test.db")
    else:
        database = DatabaseOperation("contacts.db")
    return web_app, database


app_instance, database_instance = app_factory()

config_routes(app_instance, database_instance)


if __name__ == "__main__":
    app_instance.run()
