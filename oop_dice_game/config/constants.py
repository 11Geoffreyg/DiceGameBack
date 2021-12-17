import os

os.environ['NB_DICE_SIDE'] = 6
os.environ['DEFAULT_DICES_NB'] = 5

os.environ['SCORING_DICE_VALUE_LIST'] = [1, 5] # List of the side values of the dice who trigger a standard score
os.environ['SCORING_MULTIPLIER_LIST'] = [100, 50] # List of multiplier for standard score

os.environ['THRESHOLD_BONUS'] = 3 # Threshold of the triggering for bonus in term of occurrence of the same slide value
os.environ['STANTDARD_BONUS_MULTIPLIER'] = 100
os.environ['ACE_BONUS_MULTIPLIER'] = 1000 # Special multiplier for aces bonus

os.environ['DEFAULT_WINNING_SCORE'] = 200

os.environ["HOST_NAME"] = "localhost"
os.environ["PORT"] = "8000"