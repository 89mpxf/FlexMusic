# Import dependencies
from socket import socket
from time import sleep

# Import local dependencies
from .util import log
from .splash import splash
from .session.session_manager import SessionManager
from .session.session import Session
from .helper.runtime_helper import RuntimeHelper

def runtime(server: socket, compat_signature: tuple[str, int, int, int], keyring: tuple, config: dict, debug: bool = False):
    if debug:
        log("runtime", "Runtime successfully started.")
        log("runtime", "Initializing session manager...")
    session_manager = SessionManager(config["handshake_failure_cooldown"])
    if debug:
        log("runtime", "Displaying splash screen...")
    splash(config, compat_signature, debug)
    if debug:
        log("runtime", "Starting runtime helper...")
    runtime_helper = RuntimeHelper(compat_signature, session_manager, config, debug).start()
    if debug:
        log("runtime", "Entering runtime loop...")
    server.listen(config["max_connections"])
    while True:
        try:
            conn, addr = server.accept()
            if len(session_manager) + 1 > config["max_connections"]:
                if debug:
                    log("runtime/loop", "Connection rejected from " + addr[0] + ":" + str(addr[1]) + " (max connections reached)")
                conn.close()
                continue
            if session_manager.check_flagged(addr[0]):
                if debug:
                    log("runtime/loop", "Connection rejected from " + addr[0] + ":" + str(addr[1]) + " (handshake failure cooldown active)")
                conn.close()
                continue
            if debug:
                log("runtime/loop", "Connection accepted from " + addr[0] + ":" + str(addr[1]))
            session = Session(conn, addr, compat_signature, keyring, session_manager, config, debug)
            session_manager.create_session(session)
            session.start()
            sleep(0.06)
        except KeyboardInterrupt:
            if debug:
                log("runtime/loop", "Keyboard interrupt detected. Initiating shutdown...")
            for session in session_manager:
                if debug:
                    log("runtime/loop", "Closing session #" + str(session.id) + f" ({session.address[0]}:{str(session.address[1])})...")
                session.client.close()
                session.join()
            if debug:
                log("runtime/loop", "Closing server socket...")
            server.close()
            break
        except:
            raise
    if debug:
        log("runtime", "Ending runtime...")
    return
        