# Import dependencies
from os.path import exists

# Import local dependencies
from .tui.main import main_menu
from .util import clear, load_auth_table
from ...bootstrap.configuration import load_configuration

def auth_manager(compat_signature: tuple[str, int, int, int]):
    min_password_length = load_configuration()["auth_min_password_length"]
    auth_table = load_auth_table(min_password_length)
    if auth_table is not None:
        print('\033[?25l', end="")
        if exists("auth"):
            main_menu(compat_signature, min_password_length, auth_table)
            clear()
            print("The FlexMusic server authentication manager exited successfully.\033[?25h")
        else:
            print("Please start the FlexMusic server for the first time before accessing the authentication manager.")
    else:
        print("Please start the FlexMusic server for the first time before accessing the authentication manager.")
    return