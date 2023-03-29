# Import dependencies
from bcrypt import checkpw

# Import local dependencies
from ....util import log
from ...com import InterpreterReturn

def _authenticate(interpreter, username: str, password: str) -> tuple[bool, str | None]:
    try:
        return checkpw(password.encode(), interpreter.config["auth_table"][username]), username
    except:
        return False, None

def main(interpreter, username: str, password: str):
    if interpreter.config["auth_method"] == "system":
        from simplepam import authenticate
        if authenticate(username, password):
            interpreter.current_user = username
            if interpreter.debug:
                log(f"session-{interpreter.id}/interpreter/auth", f"User '{username}' authenticated successfully.")
                log(f"session-{interpreter.id}/interpreter", f"Command AUTH returned 150.")
            interpreter.client.send(interpreter.cipher.encrypt("150 Authentication successful.\r\n".encode()))
            raise InterpreterReturn
        else:
            interpreter.client.send(interpreter.cipher.encrypt("151 Authentication failed.\r\n".encode()))
    elif interpreter.config["auth_method"] == "auth":
        result, interpreter.current_user = _authenticate(interpreter, username, password)
        if result:
            if interpreter.debug:
                log(f"session-{interpreter.id}/interpreter/auth", f"User '{username}' authenticated successfully.")
                log(f"session-{interpreter.id}/interpreter", f"Command AUTH returned 150.")
            interpreter.client.send(interpreter.cipher.encrypt("150 Authentication successful.\r\n".encode()))
            raise InterpreterReturn
        else:
            if interpreter.debug:
                log(f"session-{interpreter.id}/interpreter", f"Command AUTH returned 151.")
            interpreter.client.send(interpreter.cipher.encrypt("151 Authentication failed.\r\n".encode()))