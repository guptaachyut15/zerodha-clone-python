import hashlib
from src.utils.config import SALT


def get_hash(string_to_hash):
    hasher = hashlib.sha256
    # adding a secret salt before hashing
    salted_string = SALT + string_to_hash
    return hasher(salted_string.encode("utf-8")).hexdigest()
