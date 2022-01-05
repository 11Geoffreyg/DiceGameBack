from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
import requests


class Server:
    _server = None

    # When a server is instancied, it creates a new server
    def __init__(self, host_name='localhost', port=8000):
        self._host_name = host_name
        self._port = port

    def _http_server(self, handler=SimpleHTTPRequestHandler):
        server_address = (self._host_name, self._port)
        self._server = HTTPServer(server_address, handler)
        self._server.serve_forever()

    def run(self):
        try:
            print("Server started http://%s:%s/ (Press CTRL+C to quit)" % (self._host_name, self._port))
            self._http_server()
        except KeyboardInterrupt:
            self._server.server_close()
            pass
