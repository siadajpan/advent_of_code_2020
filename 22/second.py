from typing import Tuple, List

import numpy as np

from utils.utils import read_input_blocks


def recursion_game(cards1, cards2, history: Tuple[List[Tuple[int, ...]], List[Tuple[int, ...]]]):
    if cards1 == [] or cards2 == []:
        return cards1, cards2, cards2 == []

    if tuple(cards1) in history[0] or tuple(cards2) in history[1]:
        raise RecursionError('player 1 wins by repeating history', 'cards1', cards1, 'cards2', cards2, 'history', history)
    # add cards to history
    history[0].append(tuple(cards1))
    history[1].append(tuple(cards2))
    # get cards for both players
    c1, c2 = cards1.pop(0), cards2.pop(0)

    # check if players have enough cards to play recursion game
    if c1 > len(cards1) or c2 > len(cards2):
        return c1, c2, c1 > c2

    # copy their cards
    cards1_copy = cards1[:c1].copy()
    cards2_copy = cards2[:c2].copy()

    winner1 = True
    # initialize some dummy history
    history_rec = ([(0, 0)], [(0, 0)])
    while cards1_copy != [] and cards2_copy != []:
        try:
            c1_rec, c2_rec, winner1 = recursion_game(cards1_copy, cards2_copy, history_rec)
        except RecursionError:
            winner1 = True
            break
        if winner1:
            cards1_copy += [c1_rec, c2_rec]
        else:
            cards2_copy += [c2_rec, c1_rec]
    return c1, c2, winner1


if __name__ == '__main__':
    players = read_input_blocks('input_maarten')
    cards_1 = [int(p1) for p1 in players[0][1:]]
    cards_2 = [int(p2) for p2 in players[1][1:]]

    history = ([(0, 0)], [(0, 0)])
    while cards_2 != [] and cards_1 != []:
        c1, c2, winner1 = recursion_game(cards_1, cards_2, history)
        if winner1:
            cards_1 += [c1, c2]
        else:
            cards_2 += [c2, c1]

    winner = cards_1 if len(cards_1) else cards_2
    score = sum([(len(winner) - i) * card for i, card in enumerate(winner)])
    print(score)
