# Import dependencies
from socket import socket

# Import local dependencies
from .util import log
from .splash import splash

def runtime(server: socket, compat_signature: tuple[str, int, int, int], config: dict, debug: bool = False):
    if debug:
        log("runtime", "Runtime successfully started.")
    splash(config, compat_signature, debug)