from models.Game import Game
import json


def index_controller():
    return json.dumps(Game().return_state())


def game_controller():
    # changes performed to object
    game = Game()
    return json.dumps(game.return_state())


def settings_controller():
    return {
        "settings": "Voici le rendu #2"
    }
