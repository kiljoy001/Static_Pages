from dotenv import load_dotenv, dotenv_values, find_dotenv
import logging
import os


def load_config(filepath: str, expected_variables: list) -> bool:
    """
    Loads configuration from .env.secrets file into the OS environment.
    Returns True if all expected variables were successfully loaded, False otherwise.
    """
    logging.basicConfig(filename="config.log", encoding="utf8", level=logging.DEBUG)

    dotenv_path = find_dotenv(filepath)
    if not dotenv_path:
        logging.error("Configuration file not found: %s", filepath)
        raise FileNotFoundError("Configuration file not found: %s" % filepath)

    try:
        load_dotenv(dotenv_path=dotenv_path)
        config_values = dotenv_values(dotenv_path)
        for variable in expected_variables:
            if variable not in config_values:
                logging.error("Missing configuration variable %s", variable)
                return False
            if not config_values[variable]:
                logging.error("Missing configuration value for %s", variable)
                return False
        return True
    except Exception as error:
        logging.error("Unable to load configuration at %s: %s", dotenv_path, error)
        return False
