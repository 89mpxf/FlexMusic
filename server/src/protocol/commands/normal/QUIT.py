# Import local dependencies
from ....util import log
from ...com import InterpreterReturn

def main(interpreter):
    if interpreter.debug:
        log(f"session-{interpreter.id}/interpreter", f"Command QUIT returned 200.")
    interpreter.client.send(interpreter.cipher.encrypt("200 Goodbye.\r\n".encode()))
    raise InterpreterReturn