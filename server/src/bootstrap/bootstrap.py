# Import dependencies
from sys import argv

# Import local dependencies
from ..util import log
from .server import create_server

def bootstrap_server():
    debug = "--debug" in argv
    if debug:
        log("bootstrap", "Debug mode activated.")
    server = create_server(debug)
    