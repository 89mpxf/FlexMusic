# Import dependencies
from sys import argv

# Import local dependencies
from ..util import log
from .server import create_server
from ..runtime import runtime
from .configuration import load_configuration

def bootstrap_server():
    debug = "--debug" in argv
    if debug:
        log("bootstrap", "Debug mode activated.")
    config = load_configuration(debug)
    server = create_server(debug)
    if debug:
        log("bootstrap/create_server", "Server instance created.")
        log("bootstrap", "Handing off to runtime. Good luck!")
    return runtime(server, debug)