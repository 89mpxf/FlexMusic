# Import dependencies
from json import dumps

# Import local dependencies
from ....util import log

# Metadata values
__usage = "<query>"
__help_text = "Run a search operation on the selected backend"

def main(interpreter, *args: tuple[str]):
    query = ' '.join(args)
    if interpreter.selected_backend == "_":
        if interpreter.debug:
            log(f"session-{interpreter.id}/interpreter", "Command SEARCH returned 430.")
        interpreter.client.send(interpreter.cipher.encrypt("430 No operative backend selected.".encode()))
        return
    result = interpreter.backend_manager.backends[interpreter.selected_backend].search(query)
    if interpreter.debug:
        log(f"session-{interpreter.id}/interpreter", "Command SEARCH returned 200.")
    interpreter.client.send(interpreter.cipher.encrypt(f"200 {dumps(result)}".encode()))