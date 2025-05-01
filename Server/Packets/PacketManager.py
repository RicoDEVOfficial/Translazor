from Packets.Client.LoginMessage import LoginMessage
from Packets.Server.LoginOKMessage import LoginOKMessage
from Packets.Server.LoginFailedMessage import LoginFailedMessage
from Packets.Server.Socket.UnknownIDMessage import UnknownIDMessage

class PacketManager:
    # client→server
    client_packets = {
        10101: LoginMessage,
    }
    # server→client
    server_packets = {
        LoginOKMessage.packet_id: LoginOKMessage,
        LoginFailedMessage.packet_id: LoginFailedMessage,
        UnknownIDMessage.packet_id: UnknownIDMessage,
    }

    @classmethod
    def parse_client(cls, pkt_id: int, payload: dict):
        pkt_cls = cls.client_packets.get(pkt_id)
        return pkt_cls.from_payload(payload) if pkt_cls else None

    @classmethod
    def make_server(cls, packet_obj):
        # packet_obj must have packet_id and to_payload()
        return packet_obj.packet_id, packet_obj.to_payload()
