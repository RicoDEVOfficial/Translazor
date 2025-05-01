from cryptography.fernet import Fernet
import json, base64

def load_key(key_b64: str):
    return base64.urlsafe_b64decode(key_b64)

class Crypto:
    def __init__(self, key_b64: str):
        key = load_key(key_b64)
        self.fernet = Fernet(base64.urlsafe_b64encode(key))

    def encrypt_packet(self, packet_bytes: bytes) -> bytes:
        return self.fernet.encrypt(packet_bytes)

    def decrypt_packet(self, token: bytes) -> bytes:
        return self.fernet.decrypt(token)