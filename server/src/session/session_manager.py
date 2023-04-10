# Import dependencies
from time import time

class SessionManager:
    def __init__(self, handshake_failure_cooldown: int):
        self.handshake_failure_cooldown: int | None = handshake_failure_cooldown
        self._sessions = []
        self._next_id = 0
        self._security_table: dict[str, float] = {}

    def __len__(self):
        return len(self._sessions)
    
    def __iter__(self):
        return iter(self._sessions)
    
    def _clean_security_table(self):
        new_table = {}
        for address in self._security_table:
            if self._security_table[address] > time():
                new_table[address] = self._security_table[address]
        self._security_table = new_table

    def create_session(self, session):
        self._sessions.append(session)
        session._smh(self._next_id)
        self._next_id += 1

    def remove_session(self, session):
        self._sessions.remove(session)

    def check_flagged(self, address: str):
        self._clean_security_table()
        try:
            if self._security_table[address] > time():
                return True
            else:
                return False
        except KeyError:
            return False

    def flag_session(self, session):
        if self.handshake_failure_cooldown is not None:
            self._security_table[session.address[0]] = time() + self.handshake_failure_cooldown
        return self.remove_session(session)