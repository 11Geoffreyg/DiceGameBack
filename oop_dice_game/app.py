from controllers.index_controller import *
from api.api import API

app = API()

appRouter = app.router('http://localhost:8080/')
server = app.server(8080)

appRouter.get("/", index_controller())
appRouter.get("/game", game_controller())
appRouter.get("/setting", setting_controller())

# appRouter.get_route(server)

print(server.server())