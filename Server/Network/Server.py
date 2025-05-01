import socket
from Network.ClientConnection import ClientConnection

class Server:
    def __init__(self, host, port, crypto_key, db_path):
        self.host = host
        self.port = port
        self.crypto_key = crypto_key
        self.db_path = db_path
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print(f"[SERVER] Listening on {self.host}:{self.port}")
        while True:
            client_sock, addr = self.sock.accept()
            print(f"[SERVER] Connection from {addr}")
            conn = ClientConnection(client_sock, addr, self.crypto_key, self.db_path)
            conn.start()
