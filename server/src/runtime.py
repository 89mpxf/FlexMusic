# Import dependencies
from socket import socket

# Import local dependencies
from .util import log

def runtime(server: socket, debug: bool = False):
    if debug:
        log("runtime", "Runtime successfully started.")