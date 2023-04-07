# Import dependencies
from bcrypt import checkpw, hashpw, gensalt
from getpass import getpass

# Import local dependencies
from ..util import clear, header, press_enter, update_auth_table

submenu_options = [
    "Change username",
    "Change password",
    "Delete user",
    "Back"
]

def change_username(compat_signature: tuple[str, int, int, int], auth_table: dict[str, bytes], username: str) -> tuple[dict[str, bytes], str]:
    try:
        while True:
            clear()
            header(compat_signature)
            print("Manage User".center(80))
            print("Press Ctrl+C to cancel.".center(80))
            print("")
            print(f"Currently managing: {username}".center(80))
            print("")
            print("Change Username".center(80))
            print("")
            print(f"{' '*25}Enter new username: ", end="")
            new_username = input()
            if len(new_username) >= 2 and len(new_username) <= 32:
                if new_username.isalnum():
                    if new_username.lower() not in [username.lower() for username in auth_table.keys()]:
                            auth_table[new_username] = auth_table.pop(username)
                            result, auth_table = update_auth_table(auth_table)
                            print("")
                            if result:
                                print(f"Successfully changed username from '{username}' to '{new_username}'.".center(80))
                                press_enter()
                                return auth_table, new_username
                            else:
                                print("Failed to update authentication table. Please try again.".center(80))
                                press_enter()
                    else:
                        print("")
                        print("Username is already taken. Please try again.".center(80))
                        press_enter()
                else:
                    print("")
                    print("Username must be alphanumeric. Please try again.".center(80))
                    press_enter()
            else:
                print("")
                print("Username must be between 2 and 32 characters long. Please try again.".center(80))
                press_enter()
    except KeyboardInterrupt:
        return auth_table, username

def change_password(compat_signature: tuple[str, int, int, int], min_password_length: int, auth_table: dict[str, bytes], username: str) -> dict[str, bytes]:
    try:
        while True:
            clear()
            header(compat_signature)
            print("Manage User".center(80))
            print("Press Ctrl+C to cancel.".center(80))
            print("")
            print(f"Currently managing: {username}".center(80))
            print("")
            print("Change Password".center(80))
            print("")
            new_password = getpass(f"{' '*25}Enter new password: ")
            if len(new_password) >= min_password_length:
                pass
            else:
                print("")
                print(f"Password must be at least {min_password_length} characters long. Please try again.".center(80))
                press_enter()
                continue
            confirm_password = getpass(f"{' '*23}Confirm new password: ")
            if new_password == confirm_password:
                pass
            else:
                print("")
                print("Passwords do not match. Please try again.".center(80))
                press_enter()
                continue
            auth_table[username] = hashpw(new_password.encode(), gensalt())
            result, auth_table = update_auth_table(auth_table)
            print("")
            if result:
                print("Successfully changed password.".center(80))
                press_enter()
                return auth_table
            else:
                print("Failed to update authentication table. Please try again.".center(80))
                press_enter()
    except KeyboardInterrupt:
        return auth_table

def delete_user(compat_signature: tuple[str, int, int, int], min_password_length: int, auth_table: dict[str, bytes], username: str) -> dict[str, bytes]:
    try:
        while True:
            clear()
            header(compat_signature)
            print("Manage User".center(80))
            print("Press Ctrl+C to cancel.".center(80))
            print("")
            print(f"Currently managing: {username}".center(80))
            print("")
            print("Delete User".center(80))
            print("")
            password = getpass(f"{' '*25}Enter password: ")
            if checkpw(password.encode(), auth_table[username]):
                del auth_table[username]
                result, auth_table = update_auth_table(auth_table)
                print("")
                if result:
                    print("Successfully deleted user.".center(80))
                    press_enter()
                    return auth_table
                else:
                    print("Failed to update authentication table. Please try again.".center(80))
                    press_enter()
                    return auth_table
            else:
                print("")
                print("Incorrect password. Please try again.".center(80))
                press_enter()
    except KeyboardInterrupt:
        return auth_table

def user_submenu(compat_signature: tuple[str, int, int, int], min_password_length: int, auth_table: dict[str, bytes], username: str) -> dict[str, bytes]:
    while True:
        clear()
        header(compat_signature)
        print("Manage User".center(80))
        print("Press Ctrl+C to cancel.".center(80))
        print("")
        print(f"Currently managing: {username}".center(80))
        print("")
        offset = int((80 - max([len(val) + 2 for val in submenu_options])) / 2) - 10
        for i in range(len(submenu_options)):
            print(f"{' '*offset}{i+1}. {submenu_options[i]}")
        print("")
        print(f"{' '*offset}Please select an option (1-4): ", end="")
        try:
            if (resp := input()) == "":
                pass
            elif resp.isdigit() and 1 <= int(resp) <= 4:
                if (resp := int(resp)) == 1:
                    auth_table, username = change_username(compat_signature, auth_table, username)
                elif resp == 2:
                    auth_table = change_password(compat_signature, min_password_length, auth_table, username)
                elif resp == 3:
                    auth_table = delete_user(compat_signature, min_password_length, auth_table, username)
                if 1 < resp <= 4:
                    return auth_table
            else:
                print("")
                print("The option selected was invalid. Please try again.".center(80))
                press_enter()
        except ValueError:
            print("")
            print("The option selected was invalid. Please try again.".center(80))
            press_enter()

def login_prompt(compat_signature: tuple[str, int, int, int], min_password_length: int, auth_table: dict[str, bytes], username: str) -> dict[str, bytes]:
    try:
        while True:
            clear()
            header(compat_signature)
            print("Manage User".center(80))
            print("Press Ctrl+C to cancel.".center(80))
            print("")
            print(f"Please login as '{username}' to continue.".center(80))
            print("")
            if checkpw(getpass(prompt=f"{' '*30}Password: ").encode(), auth_table[username]):
                return user_submenu(compat_signature, min_password_length, auth_table, username)
            else:
                print("")
                print("The password was incorrect. Please try again.".center(80))
                press_enter()
    except KeyboardInterrupt:
        return auth_table
    except:
        raise
    
def manage_user_page(compat_signature: tuple[str, int, int, int], min_password_length: int, auth_table: dict[str, bytes]) -> dict[str, bytes]:
    try:
        while True:
            clear()
            header(compat_signature)
            print("Manage User".center(80))
            print("Press Ctrl+C to cancel.".center(80))
            print("")
            offset = int((80 - max([len(val) for val in auth_table.keys()])) / 2) - 2
            lookup_table = {}
            for i, username in enumerate(auth_table.keys()):
                print(f"{' '*offset}{i + 1}. {username}")
                lookup_table[i] = username
            print("")
            print(f"{' '*(offset - 5)}Select user (1-{len(auth_table.keys())}): ", end="")
            if (resp := input()).isdigit() and 1 <= int(resp) <= len(auth_table.keys()):
                auth_table = login_prompt(compat_signature, min_password_length, auth_table, lookup_table[int(resp) - 1])
            else:
                print("")
                print("The option selected was invalid. Please try again.".center(80))
                press_enter()
    except KeyboardInterrupt:
        pass
    except:
        raise
    return auth_table