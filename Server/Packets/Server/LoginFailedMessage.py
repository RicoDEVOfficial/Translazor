class LoginFailedMessage:
    packet_id = 20102

    def __init__(self, reason: str):
        self.reason = reason

    def to_payload(self):
        return {"reason": self.reason}
