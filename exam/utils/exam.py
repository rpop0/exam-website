from hashlib import sha512
from uuid import uuid4


def generate_key(first_name, last_name):
    salt = uuid4().hex
    hashed = sha512((first_name+last_name+salt).encode("utf-8")).hexdigest()
    return hashed[:15]