import hashlib


def generate_password_hash(username: str, password: str, realm: str, random_value: str) -> str:
    """Generate a password hash using MD5 hashing algorithm."""
    pwd_phrase = f"{username}:{realm}:{password}".encode('utf-8')
    pwd_hash = hashlib.md5(pwd_phrase).hexdigest().upper()
    pass_phrase = f"{username}:{random_value}:{pwd_hash}".encode('utf-8')
    return hashlib.md5(pass_phrase).hexdigest().upper()
