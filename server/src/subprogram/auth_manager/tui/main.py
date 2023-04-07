# Import local dependencies
from ..util import clear, header
from .create import create_user_page
from .manage import manage_user_page

def main_menu(compat_signature: tuple[str, int, int, int], min_password_length: int, auth_table: dict[str, bytes]):
    options = {
        1: "Create a new user",
        2: "Modify/delete an existing user",
        3: "Exit"
    }
    while True:
        clear()
        header(compat_signature)
        print("Main Menu".center(80))
        print("")
        offset = int((80 - max([len(val) + 2 for val in options.values()])) / 2)
        for key, value in options.items():
            print(f"{' '*offset}{key}. {value}")
        print("")
        print(f"{' '*offset}Please select an option (1-3): ", end="")
        try:
            i = int(input())
            if i == 1:
                auth_table = create_user_page(compat_signature, min_password_length, auth_table)
            if i == 2:
                auth_table = manage_user_page(compat_signature, min_password_length, auth_table)
            if i == 3:
                return
        except KeyboardInterrupt:
            return
        except Exception as e:
            if e.__traceback__.tb_next is not None:
                raise e
        