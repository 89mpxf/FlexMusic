# Import local dependencies
from ....common import log

# Metadata values
__usage = "<command>"
__help_text = "Displays help"

def main(interpreter, command: str = None):
    if command is not None:
        try:
            interpreter.client.send(interpreter.cipher.encrypt(f"200 Help for {command}:\r\nUsage: {command} {interpreter.commands['meta'][interpreter.interpreter_mode][command]['usage']}\r\n{interpreter.commands['meta'][interpreter.interpreter_mode][command]['help_text']}".encode()))
            if interpreter.debug:
                log(f"session-{interpreter.id}/interpreter", f"Command HELP returned 200.")
        except:
            interpreter.client.send(interpreter.cipher.encrypt(f"420 Command {command} not found.\r\n".encode()))
            if interpreter.debug:
                log(f"session-{interpreter.id}/interpreter", f"Command HELP returned 420.")
    else:
        interpreter.client.send(interpreter.cipher.encrypt("200 Available commands:\r\n".encode() + "\r\n".join([str(command + ' - ' + interpreter.commands["meta"][interpreter.interpreter_mode][command]["help_text"]) for command in interpreter.commands['meta'][interpreter.interpreter_mode]]).encode() + "\r\nRun HELP <command> for more information.\r\n".encode()))
        if interpreter.debug:
            log(f"session-{interpreter.id}/interpreter", f"Command HELP returned 200.")