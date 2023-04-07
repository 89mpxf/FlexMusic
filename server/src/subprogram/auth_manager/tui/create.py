# Import dependencies
from getpass import getpass

# Import local dependencies
from ..util import clear, header, press_enter, append_auth_table

prompts = [
    "Enter username",
    "Enter password",
    "Confirm password"
]

def create_user_page(compat_signature: tuple[str, int, int, int], min_password_length: int, auth_table: dict[str, bytes]) -> dict[str, bytes]:
    try:
        while True:
            clear()
            header(compat_signature)
            print("Create User".center(80))
            print("Press Ctrl+C to cancel.".center(80))
            print("")
            offset = int((80 - max([len(val) + 2 for val in prompts])) / 2) - 10
            for i in range(len(prompts)):
                if i == 0:
                    print(f"{' '*offset}{prompts[i]}: ", end="")
                    resp = input()
                else:
                    resp = getpass(f"{' '*offset}{prompts[i]}: ")
                
                if i == 0:
                    username = resp
                    if len(username) >= 2 and len(username) <= 32:
                        if username.isalnum():
                            if username.lower() not in [username.lower() for username in auth_table.keys()]:
                                pass
                            else:
                                print("")
                                print("Username is already taken. Please try again.".center(80))
                                press_enter()
                                break
                        else:
                            print("")
                            print("Username must be alphanumeric. Please try again.".center(80))
                            press_enter()
                            break
                    else:
                        print("")
                        print("Username must be between 2 and 32 characters long. Please try again.".center(80))
                        press_enter()
                        break
                elif i == 1:
                    password = resp
                    if len(password) >= min_password_length:
                        pass
                    else:
                        print("")
                        print(f"Password needs to be atleast {min_password_length} characters long. Please try again.".center(80))
                        press_enter()
                        break
                elif i == 2:
                    confirm_password = resp
                    if password == confirm_password:
                        print("")
                        print(f"{' '*(offset)}Create new user '{username}'? [Y/n]: ", end="")
                        confirm = input()
                        try:
                            if confirm.lower() == "y" or confirm.lower() == "":
                                result, auth_table = append_auth_table(auth_table, username, password)
                                if not result:
                                    print("")
                                    print("Failed to update the authentication table. Please try again".center(80))
                                    press_enter()
                                    break
                                else:
                                    print("")
                                    print("Successfully created new user.".center(80))
                                    press_enter()
                                    return auth_table
                            elif confirm.lower() == "n":
                                break
                            else:
                                print("")
                                print("Invalid response. Please try again.".center(80))
                                press_enter()
                                break
                        except:
                            print("")
                            print("Invalid response. Please try again.".center(80))
                            press_enter()
                            break
                    else:
                        print("")
                        print("Passwords do not match. Please try again.".center(80))
                        press_enter()
                        break

    except KeyboardInterrupt:
        pass
    return auth_table