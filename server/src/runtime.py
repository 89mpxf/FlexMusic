# Import dependencies
from socket import socket

# Import local dependencies
from .util import log
from .splash import splash
from .session.session_manager import SessionManager
from .session.session import Session

def runtime(server: socket, compat_signature: tuple[str, int, int, int], keyring: tuple, config: dict, debug: bool = False):
    if debug:
        log("runtime", "Runtime successfully started.")
        log("runtime", "Initializing session manager...")
    session_manager = SessionManager()
    if debug:
        log("runtime", "Displaying splash screen...")
    splash(config, compat_signature, debug)
    if debug:
        log("runtime", "Entering runtime loop...")
    server.listen(5)
    while True:
        conn, addr = server.accept()
        if debug:
            log("runtime/loop", "Connection accepted from " + addr[0] + ":" + str(addr[1]))
        session = Session(conn, addr, compat_signature, keyring, session_manager, config, debug)
        session_manager.create_session(session)
        session.start()
        