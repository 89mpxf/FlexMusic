# Import dependencies
from os.path import exists
from platform import system

# Import local dependencies
from ..util import log

default_configuration = [
    "",
    "# FlexMusic Server Configuration File",
    "# ONLY MODIFY THIS FILE IF YOU KNOW WHAT YOU ARE DOING",
    "",
    "# Host/port to listen on",
    "host = 0.0.0.0",
    "port = 8900",
    "",
    "# FmLTP authentication method",
    "# By default, this is set to 'auth'. A local index of users will be created and used to authenticate clients.",
    "# You can set this to 'none' to disable authentication if you wish, however, this is highly discouraged.",
    "# Additionally, if you are running your server on Linux, you can set this to 'system' to use PAM authentication.",
    "auth_method = auth",
    "",
    "# Minimum password length for users",
    "# By default, this is set to 8. This has no effect if auth_method is set to anything other than 'auth'.",
    "auth_min_password_length = 8",
    "",
    "# Encryption key size",
    "# By default, this is set to 1024. Other recommended options include 512 or 2048",
    "# NOTE: Lowering this value will make the FlexMusic server less secure, but may increase performance",
    "# NOTE: Increasing this value will make the FlexMusic server more secure, but may decrease performance",
    "# NOTE: Clients refer to this value when generating their own keypairs",
    "key_size = 1024",
    "",
    "# Handshake client timeout",
    "# By default, this is set to 5. This is the number of seconds the server will wait for a client to respond prior to the interpreter starting.",
    "# NOTE: If this value is set to 0, the server will wait indefinitely for a client to respond during this time. This is not recommended.",
    "handshake_client_timeout = 5",
    "",
    "# Maximum concurrent connections",
    "# By default, this is set to 32. This is the maximum number of connections the server will handle at any given time.",
    "# NOTE: Stability with values higher than the default is not guaranteed, though should work in theory.",
    "# NOTE: This value must be greater than 0.",
    "max_connections = 32",
    "",
    "# Handshake failure cooldown",
    "# By default, this is set to 300. This is the number, in seconds, the server will wait before allowing a client to reattempt a failed handshake.",
    "# Clients are flagged on a per-IP basis, and connections from the same IP will be blocked for this duration.",
    "# This is an additional security measure put in place to prevent spam access to the server.",
    "# NOTE: Setting this value to 0 will disable this feature. This is highly discouraged.",
    "handshake_failure_cooldown = 300",
    "",
]

def create_configuration(debug: bool = False) -> bool:
    if debug:
        log("bootstrap/configuration/creator", "Creating configuration from default template...")
    try:
        if debug:
            log("bootstrap/configuration/creator", "Template size: " + str(sum([int(len(line) + 1) for line in default_configuration])) + " bytes, " + str(len(default_configuration)) + " lines.")
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
    conf_keys = ["host", "port", "key_size", "auth_method", "auth_min_password_length"]
    for key in conf_keys:
        if key not in config:
            if debug:
                log("bootstrap/configuration/validator", f"FATAL! Configuration missing '{key}' key.")
            return None
    
    config["port"] = int(config["port"])
    if config["port"] < 1 or config["port"] > 65535:
        if debug:
            log("bootstrap/configuration/validator", "FATAL! Invalid port number.")
        return None
    
    if config["auth_method"] not in ["auth", "none", "system"] or config["auth_method"] == "system" and system() != "Linux":
        if debug:
            log("bootstrap/configuration/validator", "FATAL! Invalid authentication method.")
        return None

    config["key_size"] = int(config["key_size"])

    config["auth_min_password_length"] = int(config["auth_min_password_length"])
    if config["auth_min_password_length"] < 1:
        if debug:
            log("bootstrap/configuration/validator", "FATAL! Invalid minimum password length.")
        return None
    
    config["handshake_client_timeout"] = int(config["handshake_client_timeout"])
    if config["handshake_client_timeout"] <= 0:
        config["handshake_client_timeout"] = None

    config["max_connections"] = int(config["max_connections"])
    if config["max_connections"] <= 0:
        if debug:
            log("bootstrap/configuration/validator", "FATAL! Invalid maximum connections value.")
        return None
    
    config["handshake_failure_cooldown"] = int(config["handshake_failure_cooldown"])
    if config["handshake_failure_cooldown"] <= 0:
        config["handshake_failure_cooldown"] = None
    
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
    try:
        config = validate_configuration(config, debug)
    except KeyError as e:
        if debug:
            log("bootstrap/configuration", f"FATAL! Configuration missing {e.__str__()} key.")
        return None
    except ValueError as e:
        if debug:
            log("bootstrap/configuration", f"FATAL! Configuration value type conversion failed.")
        return None
    except:
        raise
    if not config:
        return None
    if debug:
        log("bootstrap/configuration", "Configuration loaded successfully.")
    return config
        