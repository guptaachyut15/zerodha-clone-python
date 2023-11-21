import os
from dotenv import load_dotenv

load_dotenv()


def get_config(name):
    return os.getenv(name)


MONGODB_CONNECTION_STRING = get_config("MONGODB_CONNECTION_STRING")
LOG_LEVEL = get_config("LOG_LEVEL")
JWT_SECRET_KEY = get_config("JWT_SECRET_KEY")
SALT = get_config("SALT")
