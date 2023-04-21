# Import local dependencies
from ....util import log

# Metadata values
__usage = "<backend>"
__help_text = "Select an operative backend mode"

def main(interpreter, operative: str):
    if operative not in interpreter.backend_manager.backends.keys():
        if interpreter.debug:
            log(f"session-{interpreter.id}/interpreter", "Command SELECT returned 431.")
        interpreter.client.send(interpreter.cipher.encrypt(f"431 Invalid operative backend '{operative}'".encode()))
        return
    elif operative == interpreter.selected_backend:
        if interpreter.debug:
            log(f"session-{interpreter.id}/interpreter", "Command SELECT returned 200.")
        interpreter.client.send(interpreter.cipher.encrypt(f"200 Operative backend '{operative}' already selected.".encode()))
        return
    interpreter.selected_backend = operative
    if interpreter.debug:
        log(f"session-{interpreter.id}/interpreter", "Command SELECT returned 200.")
    interpreter.client.send(interpreter.cipher.encrypt(f"200 Operative backend '{operative}' selected successfully.".encode()))
    return