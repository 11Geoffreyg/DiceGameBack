import random

NB_DICE_SIDE = 6  # Nb of side of the Dices
SCORING_DICE_VALUE_LIST = [1, 5]  # List of the side values of the dice who trigger a standard score
SCORING_MULTIPLIER_LIST = [100, 50]  # List of multiplier for standard score
DEFAULT_DICES_NB = 5

THRESHOLD_BONUS = 3  # Threshold of the triggering for bonus in term of occurrence of the same slide value
STD_BONUS_MULTIPLIER = 100  # Standard multiplier for bonus
ACE_BONUS_MULTIPLIER = 1000  # Special multiplier for aces bonus
DEFAULT_WINNING_SCORE = 2000


# return a list of dices value occurrence for a roll of nb_dice_to_roll dices
def roll_dice_set(nb_dice_to_roll, player):
    dice_value_occurrence_list = [0] * NB_DICE_SIDE
    for n in range(nb_dice_to_roll):
        dice_value = random.randint(1, NB_DICE_SIDE)
        dice_value_occurrence_list[dice_value - 1] += 1

    player['rolls'] += 1
    return dice_value_occurrence_list


def analyse_bonus_score(dice_value_occurrence_list, player):
    scoring_dices = []
    score = 0
    for side_value_index, dice_value_occurrence in enumerate(dice_value_occurrence_list):
        nb_of_bonus = dice_value_occurrence // THRESHOLD_BONUS
        if nb_of_bonus > 0:
            if side_value_index == 0:
                bonus_multiplier = ACE_BONUS_MULTIPLIER
            else:
                bonus_multiplier = STD_BONUS_MULTIPLIER

            player['bonus'] += 1
            score += nb_of_bonus * bonus_multiplier * (side_value_index + 1)
            dices_left = dice_value_occurrence_list[side_value_index] % THRESHOLD_BONUS
            nb_scoring_dices = dice_value_occurrence_list[side_value_index] - dices_left
            dice_value_occurrence_list[side_value_index] = dices_left
            scoring_dices.append([side_value_index + 1, nb_scoring_dices])

    return score, dice_value_occurrence_list, scoring_dices


def analyse_standard_score(dice_value_occurrence_list):
    score = 0
    scoring_dices = []

    for scoring_value, scoring_multiplier in zip(SCORING_DICE_VALUE_LIST, SCORING_MULTIPLIER_LIST):
        score += dice_value_occurrence_list[scoring_value - 1] * scoring_multiplier

        if dice_value_occurrence_list[scoring_value - 1] != 0:
            scoring_dices.append([scoring_value, dice_value_occurrence_list[scoring_value - 1]])
            dice_value_occurrence_list[scoring_value - 1] = 0

    return score, dice_value_occurrence_list, scoring_dices


def analyse_score(dice_value_occurrence_list, player):
    bonus_score, dice_value_occurrence_list, bonus_scoring_dices = analyse_bonus_score(dice_value_occurrence_list, player)
    standard_score, dice_value_occurrence_list, standard_scoring_dices = analyse_standard_score(dice_value_occurrence_list)

    scoring_dices = bonus_scoring_dices
    scoring_dices += standard_scoring_dices

    return bonus_score + standard_score, dice_value_occurrence_list, scoring_dices


def can_player_continue(dice_value_occurrence_list, score):
    nb_dices_left = 0

    for n in dice_value_occurrence_list:
        nb_dices_left += n

    if nb_dices_left == 0 or score == 0:
        return False, 0

    return True, nb_dices_left


def does_player_continue(can_play):
    if not can_play:
        return False

    wanna_play = input('Do you want to continue ? (y/n)')
    while wanna_play != 'y' and wanna_play != 'n':
        wanna_play = input('Do you want to continue ? (y/n)')

    if wanna_play == 'y':
        return True

    elif wanna_play == 'n':
        return False


def manage_players():
    player_count = int(input('How many players ?'))
    player_list = {}
    nb_player = 1

    for n in range(player_count):
        name = input('Player ' + str(nb_player) + ' what is your name ?')
        player_list[nb_player - 1] = {
            'name': name,
            'score': 0,
            'rolls': 0,
            'bonus': 0,
            'lost_points': 0,
            'has_won': False
        }
        nb_player = nb_player + 1

    return player_list


def has_player_won(score):
    if score >= DEFAULT_WINNING_SCORE:
        return True
    return False


def turn_counter(turn_count):
    turn_count += 1
    return turn_count


def player_turn(players):
    player_iteration = 0
    nb_dices = DEFAULT_DICES_NB
    has_won = False

    for id in players:
        wanna_play = True
        player_turn_score = 0

        while wanna_play:
            input(players[id]['name'] + ' ready ?')
            dice_value_occurrence_list = roll_dice_set(nb_dices, players[id])
            [roll_score, dice_value_occurrence_list, scoring_dices] = analyse_score(dice_value_occurrence_list,
                                                                                    players[id])
            [can_play, nb_dices] = can_player_continue(dice_value_occurrence_list, roll_score)
            print('Scoring dices : ', scoring_dices, '. You have potentially ', roll_score, ' points. You have : ',
                  str(nb_dices), ' dice(s) left to throw.')

            player_turn_score += roll_score
            if roll_score == 0:
                players[id]['lost_points'] += player_turn_score
                player_turn_score = 0

            wanna_play = does_player_continue(can_play)

        players[id]['score'] += player_turn_score
        players[id]['has_won'] = has_player_won(players[id]['score'])

        player_iteration = player_iteration + 1
        nb_dices = DEFAULT_DICES_NB

        if players[id]['has_won']:
            has_won = True

    return has_won, players


# Manage Game
def play():
    players = manage_players()
    has_won = False

    while not has_won:
        has_won, players = player_turn(players)

    print('Stats : ', players)


# Init Game
play()

