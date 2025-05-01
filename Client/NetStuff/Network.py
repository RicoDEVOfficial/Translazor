import socket
from .Crypto.Crypto import Crypto
from .Config import cfg

class ClientNetwork:
    def __init__(self):
        self.host = cfg["server_host"]
        self.port = cfg["server_port"]
        self.crypto = Crypto(cfg["encryption_key"])
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_packet(self, packet_id: int, payload: dict):
        import json, struct
        data = json.dumps({"id": packet_id, "payload": payload}).encode()
        token = self.crypto.encrypt_packet(data)
        # prefix length
        self.sock.sendall(struct.pack("!I", len(token)) + token)

    def recv_packet(self):
        import struct, json
        # read length
        raw_len = self.sock.recv(4)
        if not raw_len: return None
        length = struct.unpack("!I", raw_len)[0]
        token = self.sock.recv(length)
        data = self.crypto.decrypt_packet(token)
        return json.loads(data)