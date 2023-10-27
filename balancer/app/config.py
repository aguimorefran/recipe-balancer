# read envs
from os import environ

from dotenv import load_dotenv

load_dotenv()

DOCKER_APP = environ.get("DOCKER_APP")
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")
DB_USER = environ.get("DB_USER")
DB_PASSWORD = environ.get("DB_PASSWORD")
DB_RESET = environ.get("DB_RESET")