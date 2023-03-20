# Import dependencies
from sys import argv, exit

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
    if not config:
        print("FlexMusic Server failed to start.\nAn error occured during configuration loading.")
        exit(1)
    server = create_server(config, debug)
    if debug:
        log("bootstrap/create_server", "Server instance created.")
        log("bootstrap", "Handing off to runtime. Good luck!")
    return runtime(server, config, debug)