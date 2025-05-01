import json
from Network.Server import Server
import os, sys
# make script’s folder the current working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    # load config
    cfg = json.load(open("config.json"))
    host = cfg["host"]
    port = cfg["port"]
    key = cfg["encryption_key"]
    db = cfg["database"]
    server = Server(host, port, key, db)
    server.start()
