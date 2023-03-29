# Import dependencies
from socket import socket
from re import findall
import traceback

# Import local dependencies
from ..util import log, print_with_time
from .load import load_commands

class InterpreterReturn(Exception):
    pass

class Interpreter:
    def __init__(self, client: socket, address: tuple[str, int], cipher, config: dict, _id: int, debug: bool = False):
        self.client: socket = client
        self.address: tuple[str, int] = address
        self.cipher = cipher
        self.config: dict = config
        self.id: int = _id
        self.debug: bool = debug

        self.commands: dict = {}
        self.current_user = None
        self.interpreter_mode = "normal"

    def _core(self):
        while True:
            input = self.cipher.decrypt(self.client.recv(1024)).decode().strip().split(" ")
            try:
                self.commands[self.interpreter_mode][input[0]](self, *input[1:])
            except InterpreterReturn:
                return
            except KeyError as e:
                if e.__traceback__.tb_next is None:
                    self.client.send(self.cipher.encrypt("400 Invalid command or operative.\r\n".encode()))
                else:
                    raise e
            except TypeError as e:
                if e.__traceback__.tb_next is None:
                    try:
                        c = [int(i) for i in findall(r"\d+", str(e))]
                        if c[0] < c[1]:
                            self.client.send(self.cipher.encrypt("410 Too many arguments passed.\r\n".encode()))
                            if self.debug:
                                log(f"session-{self.id}/interpreter", f"Command {input[0]} returned 410.")
                    except:
                        self.client.send(self.cipher.encrypt("411 Too few arguments passed.\r\n".encode()))
                        if self.debug:
                            log(f"session-{self.id}/interpreter", f"Command {input[0]} returned 411.")
                else:
                    raise e

    def run_lockdown(self):
        if self.debug:
            log(f"session-{self.id}/interpreter", f"Interpreter switched to lockdown mode successfully.")
        return self._core()
        
    def run(self):
        if self.debug:
            log(f"session-{self.id}/interpreter", f"Hooking interpreter and loading commands/operatives...")
        self.commands = load_commands()
        if self.debug:
            log(f"session-{self.id}/interpreter", f"Successfully loaded {len(self.commands['normal']) + len(self.commands['lockdown'])} commands/operatives (normal: {len(self.commands['normal'])}, lockdown: {len(self.commands['lockdown'])}).")
            log(f"session-{self.id}/interpreter", f"Successfully hooked FmLTP interpreter for session #{self.id}")
        auth = False
        self.interpreter_mode = "lockdown"
        if self.config["auth_method"] != "none":
            self.client.send(self.cipher.encrypt("100 FmLTP/1.0 Intepreter Ready.\r\nAuthentication required.\r\n".encode()))
            self.run_lockdown()
            if self.current_user is None:
                return
            if self.debug:
                log(f"session-{self.id}/interpreter", f"Interpreter broke free from lockdown mode successfully.")
            auth = True
            self.interpreter_mode = "normal"
        else:
            self.client.send(self.cipher.encrypt("100 FmLTP/1.0 Intepreter Ready\r\n".encode()))
            auth = True
            self.interpreter_mode = "normal"
        if self.current_user is None:
            print_with_time(f"Accepted connection from {self.address[0]}:{self.address[1]}.")
        else:
            print_with_time(f"Accepted connection from {self.current_user} at {self.address[0]}:{self.address[1]}.")
        return self._core()

