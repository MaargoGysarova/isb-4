import json
import logging

SETTING = {
    'hash': 'bf67709b1216cb66038f3ae5ad2b4c066be03cbb',
    'begin_digits': '220220',
    'last_digits': '5688'
}


def read_settings(path_settings: str) -> dict:
    """the function reads values from settings.json"""
    try:
        with open(path_settings) as json_file:
            settings = json.load(json_file)
        logging.info(
            f"the data of settings successfully read")
    except Exception as e:
        logging.warning(
            f"an error occurred when reading data to '{settings}' file: {str(e)}")
    return settings


def write_settings(settings: dict, path_settings: str) -> None:
    """the function writes values to settings.json"""
    try:
        with open(path_settings, 'w') as f:
            json.dump(settings, f)
        logging.info(
            f"the data of settings successfully write")
    except Exception as e:
        logging.warning(
            f"an error occurred when writing data to '{settings}' file: {str(e)}")


if __name__ == "__main__":
    path = ""
    SETTING= read_settings(path)