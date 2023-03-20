# Import dependencies
from socket import socket

# Import local dependencies
from ..util import log

class HandshakeHandler:
    def __init__(self, client: socket, address: tuple[str, int], server_compat_signature: tuple[str, int, int, int], config: dict, _id: int, debug: bool = False):
        self.client: socket = client
        self.address: tuple[str, int] = address
        self.server_compat_signature: tuple[str, int, int, int] = server_compat_signature
        self.config: dict = config
        self.id = _id
        self.debug: bool = debug

    def handshake(self) -> bool:
        self.client.settimeout(5)
        try:
            self.client.send(f"{self.server_compat_signature[0]},{self.server_compat_signature[1]}.{self.server_compat_signature[2]}.{self.server_compat_signature[3]}\r\n".encode())
            if self.debug:
                log(f"handshake/session-{self.id}", "Sent SERVER_VEX_INIT. Waiting for CLIENT_VEX_REPLY...")
            client_vex_reply = self.client.recv(1024).decode().strip()
            if self.debug:
                log(f"handshake/session-{self.id}", "Received CLIENT_VEX_REPLY.")
            client_version_friendly = client_vex_reply.split(",")[0]
            client_version_class = int(client_vex_reply.split(",")[1].split(".")[0])
            client_version_stepping = int(client_vex_reply.split(",")[1].split(".")[1])
            client_version_substepping = int(client_vex_reply.split(",")[1].split(".")[2])
            warn = [0, 0]

            # Version comparison
            if client_version_class != self.server_compat_signature[1]:
                if self.debug:
                    log(f"handshake/session-{self.id}", "Client version class does not match server version class.")
                return False
            if client_version_stepping != self.server_compat_signature[2]:
                if client_version_stepping > self.server_compat_signature[2]:
                    warn[0] = 1
                elif client_version_stepping < self.server_compat_signature[2]:
                    warn[0] = 2
            if client_version_substepping != self.server_compat_signature[3]:
                if client_version_substepping > self.server_compat_signature[3]:
                    warn[1] = 1
                elif client_version_substepping < self.server_compat_signature[3]:
                    warn[1] = 2
            if self.debug:
                log(f"handshake/session-{self.id}", "Client is compatible with this server.")

            # Key exchange
            

        except TimeoutError:
            if self.debug:
                log("handshake", "Client at " + self.address[0] + ":" + str(self.address[1]) + " timed out during handshake.")
            return False
        except:
            raise