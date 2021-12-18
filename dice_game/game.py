import manageplayers
import scoring

DEFAULT_DICES_NB = 5
DEFAULT_WINNING_SCORE = 200


def has_player_won(score):
    return score >= DEFAULT_WINNING_SCORE

def game_turn(players, game_stats):
    is_there_a_winner = False

    # every player turn
    for id in players:
        wanna_play = True
        player_turn_score = bonus_turn_count = rolls_count_in_turn = 0
        nb_dices = DEFAULT_DICES_NB

        while wanna_play:
            wanna_play, player_turn_score, bonus_turn_count, nb_dices, is_full_roll, rolls_count_in_turn, game_stats = \
                player_roll(players[id], nb_dices, player_turn_score, bonus_turn_count, rolls_count_in_turn, game_stats)

        # Store player infos
        players[id]['bonus'] += bonus_turn_count
        players[id]['score'] += player_turn_score
        players[id]['full_rolls'] += 1 if is_full_roll else 0
        players[id]['has_won'] = has_player_won(players[id]['score'])
        players[id]['rolls'] += rolls_count_in_turn

        if players[id]['has_won']:
            is_there_a_winner = True

    return is_there_a_winner, game_stats, players


def player_roll(player, nb_dices, player_turn_score, bonus_turn_count, rolls_count_in_turn, game_stats):
    input('\n-- ' + player['name'] + ', enter to throw dices.')

    # Game progress : throw dices and get scores
    dice_value_occurrence_list = scoring.roll_dice_set(nb_dices)
    roll_score, dice_value_occurrence_list, scoring_dices, bonus_count = scoring.analyse_score(dice_value_occurrence_list, player)
    nb_dices = sum(dice_value_occurrence_list)
    can_play = nb_dices != 0 and roll_score != 0
    is_full_roll = not can_play and roll_score > 0
    player_turn_score += roll_score

    print('Scoring dices : ', scoring_dices, 'Scoring : ', roll_score, '. You have potentially ', player_turn_score,
          ' points. You have : ', str(nb_dices), ' dice(s) left to throw.')

    wanna_play = manageplayers.does_player_continue(can_play)
    bonus_turn_count += bonus_count
    rolls_count_in_turn += 1

    # Manage points if lost
    if roll_score == 0:
        player['lost_points'] += player_turn_score
        player['no_point_turn'] += 1
        game_stats['total_no_points_turn'] += 1

        if player_turn_score > game_stats['max_turn_loss']['score']:
            game_stats['max_turn_loss'] = {
                'score': player_turn_score,
                'player': player['name']
            }
        player_turn_score = 0
    else:
        if player_turn_score > game_stats['max_turn_score']['score']:
            game_stats['max_turn_score'] = {
                'score': player_turn_score,
                'player': player['name']
            }

    if rolls_count_in_turn > game_stats['longest_turn']['count']:
        game_stats['longest_turn'] = {
            'count': rolls_count_in_turn,
            'player': player['name']
        }

    return wanna_play, player_turn_score, bonus_turn_count, nb_dices, is_full_roll, rolls_count_in_turn, game_stats

def show_stats(players, game_stats, total_turns_game):
    print('\n Game in : ', total_turns_game, ' turns. ')

    for id in players:
        player_status = 'win' if players[id]['has_won'] else 'lose'

        # displays for cmd
        print(players[id]['name'] + ' ' +
              player_status + ' ! Scoring ' +
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
    players = manageplayers.init_players()
    stats = scoring.game_stats()
    is_there_a_winner = False
    turn_count = 0

    while not is_there_a_winner:
        turn_count += 1
        is_there_a_winner, stats, players = game_turn(players, stats)

    players = manageplayers.players_rank(players)
    stats = scoring.compute_game_stats(players, stats, turn_count)
    show_stats(players, stats, turn_count)


# Init Game
play()

