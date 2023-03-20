# Import dependencies
from threading import Thread
from socket import socket

# Import local dependencies
from ..util import log
from ..session.session_manager import SessionManager

class Session(Thread):
    def __init__(self, client: socket, address: tuple[str, int], server_compat_signature: tuple[str, int, int, int], session_manager: SessionManager, config: dict, debug: bool = False):
        Thread.__init__(self)
        self.daemon = True

        self.client: socket = client
        self.address: tuple[str, int] = address
        self.server_compat_signature: tuple[str, int, int, int] = server_compat_signature
        self.session_manager: SessionManager = session_manager
        self.config: dict = config
        self.debug: bool = debug
        self.id = None

    def run(self):
        if self.debug:
            log("session", "Session started for " + self.address[0] + ":" + str(self.address[1]))
        while True:
            pass

    # Session Manager Hook
    # Do not call this hook directly or modify
    def _smh(self, id: int):
        self.id = id

