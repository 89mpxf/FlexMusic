# Import local dependencies
from src.bootstrap.bootstrap import bootstrap_server

# Compatiblility signature for the server.
# Do NOT modify this value.
_compat_signature = ("FlexMusic Pre-Alpha Development Server", 0, 0, 0)

if __name__ == "__main__":
    bootstrap_server(_compat_signature)
