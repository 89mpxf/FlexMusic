# Import dependencies
from threading import Thread
from time import time

# Import local dependencies
from ..session.session_manager import SessionManager
from ..util import log, print_with_time

class RuntimeHelper(Thread):
    def __init__(self, compat_signature: tuple[str, int, int, int], session_manager: SessionManager, config: dict, debug: bool = False):
        Thread.__init__(self)
        self.daemon = True
        self.compat_signature: tuple[str, int, int, int] = compat_signature
        self.session_manager: SessionManager = session_manager
        self.config: dict = config
        self.debug: bool = debug
        self._uptime_start_point: float = None

    def format_uptime_stats(self, ref: float) -> str:
        _uptime = time() - ref

        uptime = [_uptime // 86400, _uptime // 3600 % 24, _uptime // 60 % 60, _uptime % 60]
        uptime_words = ["days", "hours", "minutes", "seconds"]
        uptime_string = ""

        for i in range(len(uptime)):
            if uptime[i] > 0:
                if round(uptime[i], 0) == 1:
                    uptime_words[i] = uptime_words[i][:-1]
                uptime_string += f"{uptime[i]:.0f} {uptime_words[i]}, "
                uptime_words[i] += "s"

        return uptime_string[:-2]
        
    def run(self):
        self._uptime_start_point = time()
        while True:
            input()
            print("\033[1A", end="")
            lines = []
            lines.append(f"{self.compat_signature[0]} v{self.compat_signature[1]}.{self.compat_signature[2]}.{self.compat_signature[3]}")
            lines.append(f"Server Uptime: {self.format_uptime_stats(self._uptime_start_point)}")
            lines.append(f"Active Sessions: {len(self.session_manager)}/{self.config['max_connections']}")
            if len(self.session_manager) > 0:
                lines.append("")
                if self.config["auth_method"] == "none":
                    address_offset = max([int(1 + len(session.address[0]) + len(str(session.address[1]))) for session in self.session_manager])
                    lines.append("Address".ljust(address_offset) + " Uptime")
                    for session in self.session_manager:
                        lines.append(f"{session.address[0]}:{session.address[1]}".ljust(address_offset) + " " + self.format_uptime_stats(session.start_time))
                else:
                    username_offset = max([int(len(session.fmltp_interpreter.current_user)) for session in self.session_manager if session.fmltp_interpreter is not None and session.fmltp_interpreter.current_user is not None] + [len("(unknown)")])
                    address_offset = max([int(1 + len(session.address[0]) + len(str(session.address[1]))) for session in self.session_manager])
                    lines.append("Username".ljust(username_offset) + " Address".ljust(address_offset) + "  Uptime")
                    for session in self.session_manager:
                        if session.fmltp_interpreter is not None and session.fmltp_interpreter.current_user is not None:
                            lines.append(session.fmltp_interpreter.current_user.ljust(username_offset) + f" {session.address[0]}:{session.address[1]}".ljust(address_offset) + " " + self.format_uptime_stats(session.start_time))
                        else:
                            lines.append("(unknown)".ljust(username_offset) + f" {session.address[0]}:{session.address[1]}".ljust(address_offset) + " " + self.format_uptime_stats(session.start_time))
                    print(username_offset)
            print_with_time(*lines)