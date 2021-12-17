class Game:
    def __init__(self):
        self._players = []
        self._turn_count = 0
        self._total_rolls_game = 0
        self._total_lost_points = 0
        self._total_no_point_turns = 0
        self._total_score_game = 0
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


