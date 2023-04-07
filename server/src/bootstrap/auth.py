# Import dependencies
from os.path import exists
from getpass import getpass
from bcrypt import hashpw, gensalt

# Import local dependencies
from ..util import log

def auth_prompt(min_password_length: int, debug: bool = False) -> tuple[str, str] | tuple[None, None]:
    if debug:
        log("bootstrap/auth/initial", "Prompting user for desired username / password...")
    print("\nWelcome to FlexMusic Server!")
    print("Before your server starts for the first time, you must create a user account.")
    print("This is the account you will log into this server with using your client library.\n")
    try:
        while True:
            username = input("Username: ")
            if len(username) >= 2 and len(username) <= 32:
                if username.isalnum():
                    password = getpass("Password: ")
                    confirm_password = getpass("Confirm password: ")
                    if password == confirm_password:
                        if len(password) >= min_password_length:
                            print("")
                            while True:
                                if (yn := input(f"Create user '{username}'? (y/n): ").lower()) == "y":
                                    print("")
                                    print("Thank you! To create more users, manage users, or delete users,")
                                    print("run this server with the '--auth-manager' switch.")
                                    print("")
                                    return (username, password)
                                elif yn == "n":
                                    print("")
                                    break
                                else:
                                    pass
                        else:
                            print(f"\nPassword needs to be atleast {min_password_length} characters long. Please try again.\n")
                    else:
                        print("\nPasswords do not match. Please try again.\n")
                else:
                    print("\nUsername must be alphanumeric. Please try again.\n")
            else:
                print("\nUsername must be between 2 and 32 characters long. Please try again.\n")
    except:
        if debug:
            log("bootstrap/auth/initial", "FATAL! Failed to prompt user for credentials.")
        return (None, None)

def create_auth_table(min_password_length: int, debug: bool = False) -> bool:
    if debug:
        log("bootstrap/auth/initial", "Creating authentication table...")
    try:
        with open("auth", "w") as f:
            username, password = auth_prompt(min_password_length, debug)
            if username is None or password is None:
                raise
            f.write(f"{username}:{hashpw(password.encode(), gensalt()).decode()}")
            f.close()
        if debug:
            log("bootstrap/auth/initial", "Authentication table created successfully.")
        return True
    except:
        if debug:
            log("bootstrap/auth", "FATAL! Failed to create authentication table.")
        return False

def load_auth_table(min_password_length: int, debug: bool = False, _cancel_create_auth_table: bool = False) -> dict | None:
    if debug:
        log("bootstrap/auth", "Loading authentication table...")
    if not exists("auth") or open("auth", "r").read() == "":
        if debug:
            log("bootstrap/auth", "No authentication table found.")
        if not _cancel_create_auth_table:
            create_auth_table(min_password_length, debug)
    auth_table = {}
    try:
        with open("auth", "r") as f:
            for line in f.readlines():
                username, password_hash = line.split(":")
                auth_table[username] = password_hash.strip().encode()
            f.close()
        if debug:
            log("bootstrap/auth", f"Authentication table loaded successfully ({len(list(auth_table.keys()))} accounts).")
        return auth_table
    except:
        if debug:
            log("bootstrap/auth", "FATAL! Failed to load authentication table.")
        return None