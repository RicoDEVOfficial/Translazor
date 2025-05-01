class LoginOKMessage:
    packet_id = 20101

    def __init__(self, welcome: str):
        self.welcome = welcome

    def to_payload(self):
        return {"welcome": self.welcome}
