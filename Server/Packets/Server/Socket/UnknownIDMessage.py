class UnknownIDMessage:
    packet_id = 29999

    def __init__(self, bad_id: int):
        self.bad_id = bad_id

    def to_payload(self):
        return {"message": f"Packet ID {self.bad_id} is missing!"}
