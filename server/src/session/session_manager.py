class SessionManager:
    def __init__(self):
        self._sessions = []
        self._next_id = 0

    def __len__(self):
        return len(self._sessions)
    
    def __iter__(self):
        return iter(self._sessions)

    def create_session(self, session):
        self._sessions.append(session)
        session._smh(self._next_id)
        self._next_id += 1

    def remove_session(self, session):
        self._sessions.remove(session)