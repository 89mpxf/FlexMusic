# Import dependencies
from os.path import exists

# Import local dependencies
from ..util import log

default_configuration = [
    "",
    "# FlexMusic Server Configuration File",
    "# ONLY MODIFY THIS FILE IF YOU KNOW WHAT YOU ARE DOING",
    "",
    "# Host/port to listen on",
    "host = 0.0.0.0",
    "port = 8900"
]

def create_configuration(debug: bool = False):
    if debug:
        log("bootstrap/configuration/creator", "Creating configuration from default template...")
    with open("server.conf", "w") as file:
        file.writelines([str(line + "\n") for line in default_configuration])
        file.close()
    if debug:
        log("bootstrap/configuration/creator", "Configuration file created.")

def load_configuration(debug: bool = False):
    if debug:
        log("bootstrap/configuration", "Loading configuration...")
    if not exists("server.conf"):
        if debug:
            log("bootstrap/configuration", "Configuration file not found. Creating...")
        create_configuration(debug)
    config = {}
    config_raw = None
    with open("server.conf", "r") as file:
        config_raw = file.readlines()
        file.close()
    for line in config_raw:
        line = line.strip()
        if line.startswith("#") or line == "":
            continue
        key, value = line.split("=")
        key, value = key.strip(), value.strip()
        config[key] = value
    if debug:
        log("bootstrap/configuration", "Configuration loaded successfully.")
    return config
        