# Import local dependencies
from ..util import log

class BackendManager:
    def __init__(self, config: dict, debug: bool = False):
        self.config: dict = config
        self.debug: bool = debug

        self.backends: dict = {}

    def initialize_backends(self):
        if self.debug:
            log("bootstrap/backend", "Initializing service backends...")
        for backend in self.config["backends"]:
            if self.debug:
                log("bootstrap/backend", f"Initializing '{backend}' backend...")
            self.backends[backend] = getattr(__import__(f"src.backend.backends.{backend}", fromlist=[backend]), f"{backend.title()}Backend")(self.config, self.debug)
        if self.debug:
            log("bootstrap/backend", "Service backends initialized.")
        return
