import base64
from cryptography.fernet import Fernet

def load_key(key_b64: str) -> bytes:
    # client and server must share this same base64 key
    return base64.urlsafe_b64decode(key_b64)

class Crypto:
    def __init__(self, key_b64: str):
        key = load_key(key_b64)
        self.fernet = Fernet(base64.urlsafe_b64encode(key))

    def encrypt(self, data: bytes) -> bytes:
        return self.fernet.encrypt(data)

    def decrypt(self, token: bytes) -> bytes:
        return self.fernet.decrypt(token)
