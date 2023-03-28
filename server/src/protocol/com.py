# Import dependencies
from socket import socket
from bcrypt import checkpw
from base64 import b64decode

# Import local dependencies
from ..util import log, print_with_time

class Interpreter:
    def __init__(self, client: socket, address: tuple[str, int], cipher, config: dict, _id: int, debug: bool = False):
        self.client: socket = client
        self.address: tuple[str, int] = address
        self.cipher = cipher
        self.config: dict = config
        self.id: int = _id
        self.debug: bool = debug

        self.current_user = None

    def _authenticate(self, username: str, password: str) -> tuple[bool, str | None]:
        try:
            return checkpw(password.encode(), self.config["auth_table"][username]), username
        except:
            return False, None

    def run_lockdown(self):
        if self.debug:
            log(f"session-{self.id}/interpreter", f"Interpreter switched to lockdown mode successfully.")
        while True:
            match self.cipher.decrypt(self.client.recv(1024)).decode().strip().split(" "):
                case ["QUIT", *args]:
                    if self.debug:
                        log(f"session-{self.id}/interpreter", f"Received QUIT command.")
                    if len(args) > 0:
                        if self.debug:
                            log(f"session-{self.id}/interpreter", f"Command QUIT returned 401.")
                        self.client.send(self.cipher.encrypt("401 Too many arguments passed.\r\n".encode()))
                    else:
                        if self.debug:
                            log(f"session-{self.id}/interpreter", f"Command QUIT returned 200.")
                        self.client.send(self.cipher.encrypt("200 Goodbye.\r\n".encode()))
                        return
                case ["AUTH", *args]:
                    if self.debug:
                        log(f"session-{self.id}/interpreter", f"Received AUTH command.")

                    if len(args) > 2:
                        if self.debug:
                            log(f"session-{self.id}/interpreter", f"Command AUTH returned 401.")
                        self.client.send(self.cipher.encrypt("401 Too many arguments passed.\r\n".encode()))
                    elif len(args) < 2:
                        if self.debug:
                            log(f"session-{self.id}/interpreter", f"Command AUTH returned 402.")
                        self.client.send(self.cipher.encrypt("402 Too few arguments passed.\r\n".encode()))
                    else:
                        username = args[0]
                        password = args[1]
                        if self.config["auth_method"] == "system":
                            from simplepam import authenticate
                            if authenticate(username, password):
                                self.current_user = username
                                if self.debug:
                                    log(f"session-{self.id}/interpreter/auth", f"User '{username}' authenticated successfully.")
                                    log(f"session-{self.id}/interpreter", f"Command AUTH returned 150.")
                                self.client.send(self.cipher.encrypt("150 Authentication successful.\r\n".encode()))
                                return
                            else:
                                self.client.send(self.cipher.encrypt("151 Authentication failed.\r\n".encode()))
                        elif self.config["auth_method"] == "auth":
                            result, self.current_user = self._authenticate(username, password)
                            if result:
                                if self.debug:
                                    log(f"session-{self.id}/interpreter/auth", f"User '{username}' authenticated successfully.")
                                    log(f"session-{self.id}/interpreter", f"Command AUTH returned 150.")
                                self.client.send(self.cipher.encrypt("150 Authentication successful.\r\n".encode()))
                                return
                            else:
                                if self.debug:
                                    log(f"session-{self.id}/interpreter", f"Command AUTH returned 151.")
                                self.client.send(self.cipher.encrypt("151 Authentication failed.\r\n".encode()))
                case _:
                    self.client.send(self.cipher.encrypt("400 Invalid command or operative.\r\n".encode()))

    def run(self):
        if self.debug:
            log(f"session-{self.id}/interpreter", f"Successfully hooked FmLTP interpreter for session #{self.id}")
        auth = False
        if self.config["auth_method"] != "none":
            self.client.send(self.cipher.encrypt("100 FmLTP/1.0 Intepreter Ready.\r\nAuthentication required.\r\n".encode()))
            self.run_lockdown()
            if self.current_user is None:
                return
            if self.debug:
                log(f"session-{self.id}/interpreter", f"Interpreter broke free from lockdown mode successfully.")
            auth = True
        else:
            self.client.send(self.cipher.encrypt("100 FmLTP/1.0 Intepreter Ready\r\n".encode()))
            auth = True
        if self.current_user is None:
            print_with_time(f"Accepted connection from {self.address[0]}:{self.address[1]}.")
        else:
            print_with_time(f"Accepted connection from {self.current_user} at {self.address[0]}:{self.address[1]}.")
        while auth:
            match self.cipher.decrypt(self.client.recv(1024)).decode().strip().split(" "):
                case ["QUIT", *args]:
                    if self.debug:
                        log(f"session-{self.id}/interpreter", f"Received QUIT command.")
                    if len(args) > 0:
                        if self.debug:
                            log(f"session-{self.id}/interpreter", f"Command QUIT returned 401.")
                        self.client.send(self.cipher.encrypt("401 Too many arguments passed.\r\n".encode()))
                    else:
                        if self.debug:
                            log(f"session-{self.id}/interpreter", f"Command QUIT returned 200.")
                        self.client.send(self.cipher.encrypt("200 Goodbye.\r\n".encode()))
                        return
                case _:
                    self.client.send(self.cipher.encrypt("400 Invalid command or operative.\r\n".encode()))

