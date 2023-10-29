# read envs
from os import environ

from dotenv import load_dotenv

load_dotenv()

DOCKER_APP = environ.get("DOCKER_APP", "false")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_PORT = environ.get("DB_PORT", "5432")
DB_USER = environ.get("DB_USER", "postgres")
DB_PASSWORD = environ.get("DB_PASSWORD", "postgres")
DB_RESET = environ.get("DB_RESET", "false")
