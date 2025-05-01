import struct, json, threading
from crypto import Crypto
from Packets.PacketManager import PacketManager
from Utils.Translator import Translator

class ClientConnection(threading.Thread):
    def __init__(self, sock, addr, crypto_key, db_path):
        super().__init__(daemon=True)
        self.sock = sock
        self.addr = addr
        self.crypto = Crypto(crypto_key)
        self.translator = Translator()
        self.db_path = db_path

    def run(self):
        try:
            while True:
                # read length prefix
                raw_len = self._recv_exact(4)
                if not raw_len:
                    break
                length = struct.unpack("!I", raw_len)[0]
                token = self._recv_exact(length)
                data = self.crypto.decrypt(token)
                msg = json.loads(data)
                pkt_id, payload = msg["id"], msg["payload"]
                self.handle_packet(pkt_id, payload)
        except Exception as e:
            print(f"[{self.addr}] connection error: {e}")
        finally:
            self.sock.close()

    def _recv_exact(self, n):
        buf = b''
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                return None
            buf += chunk
        return buf

    def handle_packet(self, pkt_id, payload):
        pkt = PacketManager.parse_client(pkt_id, payload)
        if pkt is None:
            self.send_server_packet(PacketManager.server_packets[29999](pkt_id))
            return

        # LOGIN flow
        if pkt_id == LoginMessage.packet_id:
            self._handle_login(pkt)

        # TRANSLATE flow (e.g. id 10102, you could add)
        # elif pkt_id == TranslateRequest.packet_id:
        #     ...

    def _handle_login(self, pkt):
        # load DB
        import json
        with open(self.db_path, "r") as f:
            db = json.load(f)

        user = next((u for u in db["users"] if u["username"] == pkt.username and u["password"] == pkt.password), None)
        if user:
            resp = PacketManager.server_packets[20101](f"Welcome, {pkt.username}!")
        else:
            resp = PacketManager.server_packets[20102]("Invalid credentials")
        self.send_server_packet(resp)

    def send_server_packet(self, packet_obj):
        import json, struct
        pkt_id, payload = packet_obj.packet_id, packet_obj.to_payload()
        data = json.dumps({"id": pkt_id, "payload": payload}).encode()
        token = self.crypto.encrypt(data)
        self.sock.sendall(struct.pack("!I", len(token)) + token)
