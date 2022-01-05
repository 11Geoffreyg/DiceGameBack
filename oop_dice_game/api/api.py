from .router import Router
from .server import Server


class API:
    def __init__(self):
        self._server = None
        self._router = None

    def router(self, url='/') -> Router:
        self._router = Router(url)
        return self._router

    def server(self, port) -> Server:
        self._server = Server(port=port)
        self._server.run()
        return self._server
