class Stats:
    def __init__(self):
        self._mean_scoring_turn = 0
        self._mean_non_scoring_turn = 0
        self._max_turn_score = {
            'player': '',
            'score': 0
        }
        self._max_turn_loss = {
            'player': '',
            'score': 0
        }
        self._longest_turn = {
            'player': '',
            'score': 0
        }

    @property
    def mean_scoring_turn(self) -> int:
        return self._mean_scoring_turn

    @mean_scoring_turn.setter   
    def turn_count(self, value):
        self._mean_scoring_turn = value
    
    @property
    def mean_non_scoring_turn(self) -> int:
        return self._mean_non_scoring_turn

    @mean_non_scoring_turn.setter   
    def turn_count(self, value):
        self._mean_non_scoring_turn = value
    

