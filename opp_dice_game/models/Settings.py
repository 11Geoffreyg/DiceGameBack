import os

class Settings:
    def __init__(
        self, 
        dice_side = os.environ['NB_DICE_SIDE'],
        nb_dice = os.environ['DEFAULT_DICES_NB'], 
        threshold_bonus = os.environ['THRESHOLD_BONUS'], 
        winning_score = os.environ['DEFAULT_WINNING_SCORE'], 
        standard_bonus_multiplier = os.environ['STANTDARD_BONUS_MULTIPLIER']):

        self._dice_side = dice_side
        self._nb_dice = nb_dice
        self._threshold_bonus = threshold_bonus
        self._winning_score = winning_score
        self._standard_bonus_multiplier = standard_bonus_multiplier
        
    @property
    def dice_side(self) -> int:
        return self._dice_side

    @dice_side.setter   
    def dice_side(self, value):
        self._dice_side = value

    @property
    def nb_dice(self) -> int:
        return self._nb_dice

    @nb_dice.setter   
    def nb_dice(self, value):
        self._nb_dice = value

    @property
    def threshold_bonus(self) -> int:
        return self._threshold_bonus

    @threshold_bonus.setter   
    def threshold_bonus(self, value):
        self._threshold_bonus = value

    @property
    def winning_score(self) -> int:
        return self._winning_score

    @winning_score.setter   
    def winning_score(self, value):
        self._winning_score = value

    @property
    def standard_bonus_multiplier(self) -> int:
        return self._standard_bonus_multiplier

    @standard_bonus_multiplier.setter   
    def standard_bonus_multiplier(self, value):
        self._standard_bonus_multiplier = value
