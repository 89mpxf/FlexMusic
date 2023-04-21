# Import dependencies
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# Import local dependencies
from ..common import log

def create_server(config: dict, debug: bool = False) -> socket:
    if debug:
        log("bootstrap/create_server", "Creating server socket...")
    server = socket(AF_INET, SOCK_STREAM)
    if debug:
        log("bootstrap/create_server", "Setting socket options...")
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    if debug:
        log("bootstrap/create_server", "Binding server socket...")
    server.bind((config["host"], config["port"]))
    if debug:
        log("bootstrap/create_server", "Server created successfully.")
    return server