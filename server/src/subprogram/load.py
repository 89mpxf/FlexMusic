# Import dependencies
from sys import argv, exit

# Import local dependencies
from .help import help
from .auth_manager.auth_manager import auth_manager

def load_subprogram(compat_signature: tuple[str, int, int, int]):
    if "--help" in argv:
        exit(help(compat_signature))
    if "--auth-manager" in argv:
        exit(auth_manager(compat_signature))
    return