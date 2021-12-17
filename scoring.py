import random

NB_DICE_SIDE = 6  # Nb of side of the Dices
SCORING_DICE_VALUE_LIST = [1, 5]  # List of the side values of the dice who trigger a standard score
SCORING_MULTIPLIER_LIST = [100, 50]  # List of multiplier for standard score
DEFAULT_DICES_NB = 5

THRESHOLD_BONUS = 3  # Threshold of the triggering for bonus in term of occurrence of the same slide value
STD_BONUS_MULTIPLIER = 100  # Standard multiplier for bonus
ACE_BONUS_MULTIPLIER = 1000  # Special multiplier for aces bonus
DEFAULT_WINNING_SCORE = 200


# return a list of dices value occurrence for a roll of nb_dice_to_roll dices
def roll_dice_set(nb_dice_to_roll):
    dice_value_occurrence_list = [0] * NB_DICE_SIDE
    for n in range(nb_dice_to_roll):
        dice_value = random.randint(1, NB_DICE_SIDE)
        dice_value_occurrence_list[dice_value - 1] += 1

    return dice_value_occurrence_list


def analyse_bonus_score(dice_value_occurrence_list):
    scoring_dices = []
    total_bonus = 0
    score = 0

    for side_value_index, dice_value_occurrence in enumerate(dice_value_occurrence_list):
        nb_of_bonus = dice_value_occurrence // THRESHOLD_BONUS
        if nb_of_bonus > 0:
            if side_value_index == 0:
                bonus_multiplier = ACE_BONUS_MULTIPLIER
            else:
                bonus_multiplier = STD_BONUS_MULTIPLIER

            score += nb_of_bonus * bonus_multiplier * (side_value_index + 1)
            total_bonus += nb_of_bonus

            # Stores dices left to play not used in bonus
            dices_left = dice_value_occurrence % THRESHOLD_BONUS
            dice_value_occurrence_list[side_value_index] = dices_left

            # Store scoring dices
            nb_scoring_dices = dice_value_occurrence - dices_left
            scoring_dices.append([side_value_index + 1, nb_scoring_dices])

    return score, dice_value_occurrence_list, scoring_dices, total_bonus


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
    bonus_score, dice_value_occurrence_list, bonus_scoring_dices, bonus_count = analyse_bonus_score(dice_value_occurrence_list)
    standard_score, dice_value_occurrence_list, standard_scoring_dices = analyse_standard_score(dice_value_occurrence_list)

    scoring_dices = bonus_scoring_dices
    scoring_dices += standard_scoring_dices

    return bonus_score + standard_score, dice_value_occurrence_list, scoring_dices, bonus_count


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

    return True if wanna_play == "y" else False


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
            'no_point_turn': 0,
            'has_won': False,
            'full_rolls': 0
        }
        nb_player = nb_player + 1

    return player_list


def game_stats():
    return {
        'max_turn_score': {
            'score': 0,
            'player': ''
        },
        'max_turn_loss': {
            'score': 0,
            'player': ''
        },
        'total_no_points_turn': 0,
        'longest_turn': {
            'count': 0,
            'player': ''
        },
        'mean_scoring_turn': 0,
        'mean_non_scoring_turn': 0
    }


def has_player_won(score):
    return score >= DEFAULT_WINNING_SCORE


def turn_counter(turn_count):
    turn_count += 1
    return turn_count


def is_full_role(can_play, score):
    if not can_play and score > 0:
        return 1
    return 0


def is_max(number, prev_max):
    return number > prev_max


def game_turn(players, game_stats):
    has_won = False

    # every player turn
    for id in players:
        wanna_play = True
        player_turn_score = bonus_turn_count = rolls_count_in_turn = 0
        nb_dices = DEFAULT_DICES_NB

        while wanna_play:
            wanna_play, player_turn_score, bonus_turn_count, nb_dices, full_roll, rolls_count_in_turn, game_stats = \
                player_roll(players[id], nb_dices, player_turn_score, bonus_turn_count, rolls_count_in_turn, game_stats)

        # Store player infos
        players[id]['bonus'] += bonus_turn_count
        players[id]['score'] += player_turn_score
        players[id]['full_rolls'] += full_roll
        players[id]['has_won'] = has_player_won(players[id]['score'])
        players[id]['rolls'] += rolls_count_in_turn

        if players[id]['has_won']:
            has_won = True

    return has_won, game_stats, players


def player_roll(player, nb_dices, player_turn_score, bonus_turn_count, rolls_count_in_turn, game_stats):
    input('\n-- ' + player['name'] + ', enter to throw dices.')

    # Game progress : throw dices and get scores
    dice_value_occurrence_list = roll_dice_set(nb_dices)
    roll_score, dice_value_occurrence_list, scoring_dices, bonus_count = analyse_score(dice_value_occurrence_list, player)
    can_play, nb_dices = can_player_continue(dice_value_occurrence_list, roll_score)
    full_roll = is_full_role(can_play, roll_score)
    player_turn_score += roll_score

    print('Scoring dices : ', scoring_dices, 'Scoring : ', roll_score, '. You have potentially ', player_turn_score,
          ' points. You have : ', str(nb_dices), ' dice(s) left to throw.')

    wanna_play = does_player_continue(can_play)
    bonus_turn_count += bonus_count
    rolls_count_in_turn += 1

    # Manage points if lost
    if roll_score == 0:
        player['lost_points'] += player_turn_score
        player['no_point_turn'] += 1
        game_stats['total_no_points_turn'] += 1

        if is_max(player_turn_score, game_stats['max_turn_loss']['score']):
            game_stats['max_turn_loss'] = {
                'score': player_turn_score,
                'player': player['name']
            }
        player_turn_score = 0
    else:
        if is_max(player_turn_score, game_stats['max_turn_score']['score']):
            game_stats['max_turn_score'] = {
                'score': player_turn_score,
                'player': player['name']
            }

    if is_max(rolls_count_in_turn, game_stats['longest_turn']['count']):
        game_stats['longest_turn'] = {
            'count': rolls_count_in_turn,
            'player': player['name']
        }

    return wanna_play, player_turn_score, bonus_turn_count, nb_dices, full_roll, rolls_count_in_turn, game_stats


def players_rank(players):
    players = {k: v for k, v in sorted(players.items(), key=lambda item: item[1]['score'], reverse=True)}
    return players


def calculate_game_stats(players, stats, total_turns_game):
    total_score_game = 0
    total_rolls_game = 0
    total_lost_points = 0

    for id in players:
        total_score_game += players[id]['score']
        total_rolls_game += players[id]['rolls']
        total_lost_points += players[id]['lost_points']

    stats['mean_scoring_turn'] = round((total_score_game / len(players) / total_turns_game), 2)
    stats['mean_non_scoring_turn'] = round((total_lost_points / stats['total_no_points_turn']), 2) if stats['total_no_points_turn'] else 0

    return stats


def show_stats(players, game_stats, total_turns_game):
    print('\n Game in : ', total_turns_game, ' turns. ')

    for id in players:
        has_won = 'win' if players[id]['has_won'] else 'lose'

        # displays for cmd
        print(players[id]['name'] + ' ' +
              has_won + ' ! Scoring ' +
              str(players[id]['score']) + ' in ' +
              str(players[id]['rolls']) + ' roll(s) with ' +
              str(players[id]['full_rolls']) + ' full roll. ' +
              str(players[id]['bonus']) + ' bonus and ' +
              str(players[id]['lost_points']) + ' potential points lost.')

    # displays general stats for cmd
    print('\n Mean scoring turn : ' +
          str(game_stats['mean_scoring_turn']) +
          ' (' + str(total_turns_game) + ' turn(s)) \n Mean non scoring turn : ' +
          str(game_stats['mean_non_scoring_turn']) +
          ' (' + str(game_stats['total_no_points_turn']) + ' turn(s))')
    print('\nMax score in one turn : ' + str(game_stats['max_turn_score']['score']) + ' by ' + game_stats['max_turn_score']['player'])
    print('Max loss in one turn : ' + str(game_stats['max_turn_loss']['score']) + ' by ' + game_stats['max_turn_loss']['player'])
    print('Longest turn : ' + str(game_stats['longest_turn']['count']) + ' by ' + game_stats['longest_turn']['player'])


# Manage Game
def play():
    players = manage_players()
    stats = game_stats()
    has_won = False
    turn_count = 0

    while not has_won:
        turn_count = turn_counter(turn_count)
        has_won, stats, players = game_turn(players, stats)

    players = players_rank(players)
    stats = calculate_game_stats(players, stats, turn_count)
    show_stats(players, stats, turn_count)


# Init Game
play()

