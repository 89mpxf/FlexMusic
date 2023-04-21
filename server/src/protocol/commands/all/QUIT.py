# Import local dependencies
from ....common import log
from ...com import InterpreterReturn

# Metadata values
__help_text = "Closes connection to server"

def main(interpreter):
    if interpreter.debug:
        log(f"session-{interpreter.id}/interpreter", f"Command QUIT returned 200.")
    interpreter.client.send(interpreter.cipher.encrypt("200 Goodbye.\r\n".encode()))
    raise InterpreterReturn