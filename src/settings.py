# settings.py
import os

from dotenv import load_dotenv

load_dotenv("../config/.env")


class MissingEnvironmentVariable(Exception):
    pass


def get_environment_variable(variable: str) -> str:
    try:
        return os.environ[variable.upper()]
    except KeyError:
        raise MissingEnvironmentVariable(f"{variable} does not exist")
