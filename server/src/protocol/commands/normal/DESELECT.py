# Import local dependencies
from ....util import log

# Metadata values
__help_text = "Deselect the current operative backend"

def main(interpreter):
    if interpreter.selected_backend == "_":
        if interpreter.debug:
            log(f"session-{interpreter.id}/interpreter", "Command DESELECT returned 430.")
        interpreter.client.send(interpreter.cipher.encrypt("430 No operative backend selected.".encode()))
        return
    interpreter.selected_backend = "_"
    if interpreter.debug:
        log(f"session-{interpreter.id}/interpreter", "Command DESELECT returned 200.")
    interpreter.client.send(interpreter.cipher.encrypt(f"200 Operative backend deselected successfully.".encode()))