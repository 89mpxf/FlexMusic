# Import dependencies
from sys import argv, exit

# Import local dependencies
from .help import help

def load_subprogram(compat_signature: tuple[str, int, int, int]):
    if "--help" in argv:
        exit(help(compat_signature))
    return