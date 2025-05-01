import json

class LoginMessage:
    packet_id = 10101

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @classmethod
    def from_payload(cls, p):
        return cls(p["username"], p["password"])
