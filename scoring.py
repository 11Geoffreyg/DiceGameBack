import random

NB_DICE_SIDE = 6  # Nb of side of the Dices
SCORING_DICE_VALUE_LIST = [1, 5]  # List of the side values of the dice who trigger a standard score
SCORING_MULTIPLIER_LIST = [100, 50]  # List of multiplier for standard score
DEFAULT_DICES_NB = 5

THRESHOLD_BONUS = 3  # Threshold of the triggering for bonus in term of occurrence of the same slide value
STD_BONUS_MULTIPLIER = 100  # Standard multiplier for bonus
ACE_BONUS_MULTIPLIER = 1000  # Special multiplier for aces bonus

wanna_play = True


# return a list of dices value occurrence for a roll of nb_dice_to_roll dices
def roll_dice_set(nb_dice_to_roll):
    dice_value_occurrence_list = [0] * NB_DICE_SIDE
    for n in range(nb_dice_to_roll):
        dice_value = random.randint(1, NB_DICE_SIDE)
        dice_value_occurrence_list[dice_value - 1] += 1

    return dice_value_occurrence_list


def analyse_bonus_score(dice_value_occurrence_list):
    scoring_dices = []
    score = 0
    for side_value_index, dice_value_occurrence in enumerate(dice_value_occurrence_list):
        nb_of_bonus = dice_value_occurrence // THRESHOLD_BONUS
        if nb_of_bonus > 0:
            if side_value_index == 0:
                bonus_multiplier = ACE_BONUS_MULTIPLIER
            else:
                bonus_multiplier = STD_BONUS_MULTIPLIER
            score += nb_of_bonus * bonus_multiplier * (side_value_index + 1)
            dices_left = dice_value_occurrence_list[side_value_index] % THRESHOLD_BONUS
            nb_scoring_dices = dice_value_occurrence_list[side_value_index] - dices_left
            dice_value_occurrence_list[side_value_index] = dices_left
            scoring_dices.append([side_value_index + 1, nb_scoring_dices])

    return score, dice_value_occurrence_list, scoring_dices


def analyse_standard_score(dice_value_occurrence_list):
    score = 0
    for scoring_value, scoring_multiplier in zip(SCORING_DICE_VALUE_LIST, SCORING_MULTIPLIER_LIST):
        score += dice_value_occurrence_list[scoring_value - 1] * scoring_multiplier
        dice_value_occurrence_list[scoring_value - 1] = 0

    return score, dice_value_occurrence_list


def analyse_score(dice_value_occurrence_list):
    bonus_score, dice_value_occurrence_list, scoring_dices = analyse_bonus_score(dice_value_occurrence_list)
    standard_score, dice_value_occurrence_list = analyse_standard_score(dice_value_occurrence_list)

    return bonus_score + standard_score, dice_value_occurrence_list


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


def play(wanna_play, nb_dices):
    nb_dices_left = nb_dices
    while wanna_play:
        dice_value_occurrence_list = roll_dice_set(nb_dices_left)
        [final_score, dice_value_occurrence_list] = analyse_score(dice_value_occurrence_list)
        [can_play, nb_dices_left] = can_player_continue(dice_value_occurrence_list, final_score)
        print('You have potentially ', final_score, ' points. You have : ', nb_dices_left, ' dice(s) left to throw.')

        wanna_play = does_player_continue(can_play)

    print('score : ', final_score, ' list : ', dice_value_occurrence_list)


play(wanna_play, DEFAULT_DICES_NB)