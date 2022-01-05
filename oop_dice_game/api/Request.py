import json
from urllib.parse import urlparse, parse_qs
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler

from oop_dice_game.controllers.index_controller import index_controller, game_controller, settings_controller


class Request(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/?'):
            query_parameters = parse_qs(self.path[2:])
            print(query_parameters)
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(index_controller()).encode())

        if self.path.startswith('/game?'):
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(game_controller()).encode())

        if self.path.startswith('/settings?'):
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(settings_controller()).encode())
