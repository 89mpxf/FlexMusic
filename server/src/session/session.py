# Import dependencies
from threading import Thread
from socket import socket
from cryptography.fernet import InvalidToken

# Import local dependencies
from ..util import log, print_with_time
from ..session.session_manager import SessionManager
from ..handshake import HandshakeHandler
from ..protocol.com import Interpreter

class Session(Thread):
    def __init__(self, client: socket, address: tuple[str, int], server_compat_signature: tuple[str, int, int, int], keyring: tuple, session_manager: SessionManager, config: dict, debug: bool = False):
        Thread.__init__(self)
        self.daemon = True

        self.client: socket = client
        self.address: tuple[str, int] = address
        self.server_compat_signature: tuple[str, int, int, int] = server_compat_signature
        self.keyring: tuple = keyring
        self.session_manager: SessionManager = session_manager
        self.config: dict = config
        self.debug: bool = debug
        self.id = None

        self.handshake_handler = None
        self.fmltp_interpreter = None

    def run(self):
        if self.debug:
            log(f"session-{self.id}", "Session started for " + self.address[0] + ":" + str(self.address[1]))
            log(f"session-{self.id}", "Initializing handshake handler...")
        self.handshake_handler = HandshakeHandler(self.client, self.address, self.server_compat_signature, self.keyring, self.config, self.id, self.debug)
        if self.debug:
            log(f"session-{self.id}", "Starting handshake...")
        cipher = self.handshake_handler.handshake()
        if cipher is None:
            if self.debug:
                log(f"session-{self.id}", "Handshake failed. Closing connection.")
            self.client.close()
            self.session_manager.flag_session(self)
            return
        if self.debug:
            log(f"session-{self.id}", "Handshake successful. Initializing FmLTP interpreter...")
        self.fmltp_interpreter = Interpreter(self.client, self.address, cipher, self.config, self.id, self.debug)
        if self.debug:
            log(f"session-{self.id}", "Starting FmLTP interpreter...")
        self.client.settimeout(None)
        try:
            self.fmltp_interpreter.run()
        except InvalidToken:
            if self.debug:
                log(f"session-{self.id}", "Session encryption violation occured. Closing connection.")
        except:
            pass
        if self.debug:
            log(f"session-{self.id}", "FmLTP interpreter stopped. Closing connection.")
        print_with_time(f"Connection from {self.address[0]}:{self.address[1]} closed.")
        self.client.close()
        self.session_manager.remove_session(self)
        return

    # Session Manager Hook
    # Do not call this hook directly or modify
    def _smh(self, id: int):
        self.id = id

