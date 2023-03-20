# Import dependencies
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# Import local dependencies
from ..util import log

def create_server(debug: bool = False) -> socket:
    if debug:
        log("bootstrap/create_server", "Creating server socket...")
    server = socket(AF_INET, SOCK_STREAM)
    if debug:
        log("bootstrap/create_server", "Setting socket options...")
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    if debug:
        log("bootstrap/create_server", "Binding server socket...")
    server.bind(("0.0.0.0", 8900))
    return server