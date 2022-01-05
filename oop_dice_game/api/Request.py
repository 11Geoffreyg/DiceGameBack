from http.server import BaseHTTPRequestHandler


class Request(BaseHTTPRequestHandler):

    def __init__(self, url):
        self._url = url
