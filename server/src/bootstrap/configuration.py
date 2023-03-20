# Import dependencies
from os.path import exists
from sys import exit

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

def create_configuration(debug: bool = False) -> bool:
    if debug:
        log("bootstrap/configuration/creator", "Creating configuration from default template...")
    try:
        with open("server.conf", "w") as file:
            file.writelines([str(line + "\n") for line in default_configuration])
            file.close()
        if debug:
            log("bootstrap/configuration/creator", "Configuration file created.")
        return True
    except:
        if debug:
            log("bootstrap/configuration/creator", "FATAL! Failed to create configuration file.")
        return False
    
def validate_configuration(config: dict, debug: bool = False) -> dict | None:
    if "host" not in config:
        if debug:
            log("bootstrap/configuration/validator", "FATAL! Configuration missing 'host' key.")
        return None
    if "port" not in config:
        if debug:
            log("bootstrap/configuration/validator", "FATAL! Configuration missing 'port' key.")
        return None
    
    config["port"] = int(config["port"])
    return config

def load_configuration(debug: bool = False):
    if debug:
        log("bootstrap/configuration", "Loading configuration...")
    if not exists("server.conf"):
        if debug:
            log("bootstrap/configuration", "Configuration file not found. Creating...")
        if not create_configuration(debug):
            return None
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
        log("bootstrap/configuration", "Validating configuration...")
    config = validate_configuration(config, debug)
    if not config:
        return None
    if debug:
        log("bootstrap/configuration", "Configuration loaded successfully.")
    return config
        