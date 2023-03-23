# Import dependencies
from sys import argv, exit

# Import local dependencies
from ..util import log
from .server import create_server
from ..runtime import runtime
from .configuration import load_configuration
from ..crypto import generate_parameters

def bootstrap_server(compat_signature: tuple[str, int, int, int]):
    print("FlexMusic Media Server is starting...")
    debug = "--debug" in argv
    if debug:
        log("bootstrap", "Debug mode activated.")
        log("bootstrap", "Now Starting FlexMusic Server.")
        log("bootstrap", "Version: " + compat_signature[0])
        log("bootstrap", "Compatibility Class: " + str(compat_signature[1]))
        log("bootstrap", "Compatibility Stepping: " + str(compat_signature[2]))
        log("bootstrap", "Compatibility Sub-stepping: " + str(compat_signature[3]))
    config = load_configuration(debug)
    if not config:
        print("FlexMusic Server failed to start.\nAn error occured during configuration loading.")
        exit(1)
    keyring = generate_parameters(config["key_size"], debug)
    server = create_server(config, debug)
    if debug:
        log("bootstrap", "Handing off to runtime. Good luck!")
    return runtime(server, compat_signature, keyring, config, debug)