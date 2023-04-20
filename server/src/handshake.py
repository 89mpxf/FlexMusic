# Import dependencies
from socket import socket

# Import local dependencies
from .util import log
from .crypto import process_client_key

class HandshakeHandler:
    def __init__(self, client: socket, address: tuple[str, int], server_compat_signature: tuple[str, int, int, int], keyring: tuple, config: dict, _id: int, debug: bool = False):
        self.client: socket = client
        self.address: tuple[str, int] = address
        self.server_compat_signature: tuple[str, int, int, int] = server_compat_signature
        self.keyring: tuple = keyring
        self.config: dict = config
        self.id = _id
        self.debug: bool = debug

    def handshake(self):
        self.client.settimeout(self.config["handshake_client_timeout"])
        try:
            if self.debug:
                log(f"session-{self.id}/handshake", "Starting handshake...")
            self.client.send(str(server_kex_init_value := f"{self.server_compat_signature[0]},{self.server_compat_signature[1]}.{self.server_compat_signature[2]}.{self.server_compat_signature[3]}\r\n").encode())
            if self.debug:
                log(f"session-{self.id}/handshake", "Sent SERVER_VEX_INIT. Waiting for CLIENT_VEX_REPLY...")
            client_vex_reply = self.client.recv(1024).decode().strip()
            if self.debug:
                log(f"session-{self.id}/handshake", "Received CLIENT_VEX_REPLY.")
            client_version_friendly = client_vex_reply.split(",")[0]
            client_version_class = int(client_vex_reply.split(",")[1].split(".")[0])
            client_version_stepping = int(client_vex_reply.split(",")[1].split(".")[1])
            client_version_substepping = int(client_vex_reply.split(",")[1].split(".")[2])
            warn = [0, 0]

            # Version comparison
            if client_version_class != self.server_compat_signature[1]:
                if self.debug:
                    log(f"session-{self.id}/handshake", "Client version class does not match server version class.")
                return None
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
                log(f"session-{self.id}/handshake", "Client is compatible with this server.")

            # Key exchange
            if self.debug:
                log(f"session-{self.id}/handshake", "Starting key exchange...")
            self.client.send(self.keyring[1])
            if self.debug:
                log(f"session-{self.id}/handshake", "Sent SERVER_KEX_INIT. Waiting for CLIENT_KEX_ID...")
            if (cipher := process_client_key(self.client.recv(2048), self.id, self.keyring, self.debug)) is None:
                if self.debug:
                    log(f"session-{self.id}/handshake", "Client key exchange failed.")
                return None
            if self.debug:
                log(f"session-{self.id}/handshake", "Client key exchange successful. Sending SERVER_KEX_ID...")
            self.client.send(self.keyring[4])
            if self.debug:
                log(f"session-{self.id}/handshake", "Sent SERVER_KEX_ID. Waiting for CLIENT_KEX_CHAL...")
            if not cipher.decrypt(self.client.recv(2048)).decode().strip() == server_kex_init_value.strip():
                if self.debug:
                    log(f"session-{self.id}/handshake", "Client key exchange challenge failed.")
                return None
            if self.debug:
                log(f"session-{self.id}/handshake", "Key exchange successful.")
            return cipher

        except TimeoutError:
            if self.debug:
                log(f"session-{self.id}", f"Client at {self.address[0]}:{self.address[1]} timed out during handshake.")
            return None
        except:
            #raise
            if self.debug:
                log(f"session-{self.id}", f"Client at {self.address[0]}:{self.address[1]} failed to complete handshake.")
            return None