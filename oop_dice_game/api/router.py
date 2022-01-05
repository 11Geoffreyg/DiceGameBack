from .route import Route


class Router:
    def __init__(self, url):
        self._url = url
        self._routes = {
            'GET': []
        }

    def get(self, route_path, controller_handler):
        route = Route(route_path, controller_handler)
        self._routes['GET'].append(route)

    def get_route(self, server):
        print(server)
