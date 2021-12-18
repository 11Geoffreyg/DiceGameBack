from http.server import HTTPServer, SimpleHTTPRequestHandler

class Server:
    _server = None

    # When a server is instancied, it creates a new server
    def __init__(self, host_name = 'localhost', port = 8000):
        self._host_name = host_name
        self._port = port

        self._create(self._host_name, self._port)

    # This function creates a new server instance
    def _create(self, host, port):
        server_address = (host, port)
        self._server = HTTPServer(server_address, SimpleHTTPRequestHandler)

    # This function run server instance
    def run(self):
        if not self._server:
            raise ValueError('Server does not exist')

        try:
            print("Server started http://%s:%s/" % (self._host_name, self._port))
            self._server.serve_forever()
        except KeyboardInterrupt:
            pass
            self._server.server_close()