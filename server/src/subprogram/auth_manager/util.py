# Import dependencies
from os import system
from getpass import getpass
from bcrypt import hashpw, gensalt

# Import local dependencies
from ...bootstrap.auth import load_auth_table

def clear():
    if system("clear") != 0:
        system("cls")
    return

def header(compat_signature: tuple[str, int, int, int]):
    print("")
    print(f"FlexMusic Server v{compat_signature[1]}.{compat_signature[2]}.{compat_signature[3]}".center(80))
    print("Authentication Manager".center(80))
    print("")
    return

def press_enter():
    print("")
    print("Press Enter to continue.".center(80))
    getpass("")
    return

def fetch_auth_table(min_password_length: int) -> dict | None:
    auth_table = load_auth_table(min_password_length, False, True)
    if auth_table is not None:
        return auth_table
    else:
        return None
    
def update_auth_table(auth_table: dict[str, bytes]) -> tuple[bool, dict[str, bytes]]:
    try:
        with open("auth", "w") as f:
            f.seek(0)
            for _username, _password in auth_table.items():
                f.write(f"{_username}:{_password.decode()}\n")
            f.close()
        return True, auth_table
    except:
        return False, auth_table
    
def append_auth_table(auth_table: dict[str, bytes], username: str, password: str) -> tuple[bool, dict[str, bytes]]:
    auth_table[username] = hashpw(password.encode(), gensalt())
    result, auth_table = update_auth_table(auth_table)
    if not result:
        try:
            del auth_table[username]
        except:
            raise
        return False, auth_table
    else:
        return True, auth_table
