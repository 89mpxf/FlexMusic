class YoutubeBackend:
    def __init__(self, config: dict, debug: bool = False):
        self.config: dict = config
        self.debug: bool = debug

    def search(self, query: str) -> dict:
        _ret = {}
        _ret["query"] = query
        _ret["output"] = "Not implemented yet."
        return _ret
    
    def get(self, id: str) -> dict:
        _ret = {}
        _ret["output"] = "Not implemented yet."
        return _ret