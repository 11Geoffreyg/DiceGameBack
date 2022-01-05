class Game:
    def __init__(self):
        self._players = []
        self._turn_count = 0
        self._total_rolls_game = 0
        self._total_lost_points = 0
        self._total_no_point_turns = 0
        self._total_score_game = 0
        self._winner = {}
        self._settings = {}
        self._stats = {}

    def turn_counter(self):
        self._turn_count += 1
    
    def manage_players():
        print("Manage Player")

    def game_stats():
        print("Game stats")
        

    @property
    def turn_count(self) -> int:
        return self._turn_count

    @turn_count.setter   
    def turn_count(self, value):
        self._turn_count = value

    def return_state(self):
        return {
            'players': self._players,
            'turn_count': self._turn_count,
            'total_rolls_game': self._total_rolls_game,
            'total_lost_points': self._total_lost_points,
            'total_no_point_turns': self._total_no_point_turns,
            'total_score_game': self._total_score_game,
            'winner': self._winner,
            'settings': self._settings,
            'stats': self._stats
        }


