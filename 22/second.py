from typing import Tuple, List

import numpy as np

from utils.utils import read_input_blocks


def recursion_game(cards1, cards2, history: Tuple[List[Tuple[int, ...]], List[Tuple[int, ...]]]):
    print('\n\n NEW GAME \nhistory\n', history[0],'\n', history[1])
    print('cards1', cards1, '\ncards2', cards2)
    if tuple(cards1) in history[0] or tuple(cards2) in history[1]:
        raise Exception('player 1 wins by repeating history', 'c1', cards1, 'c2', cards2, 'history', history)
    history[0].append(tuple(cards1))
    history[1].append(tuple(cards2))
    # print('history\n', history[0],'\n', history[1])
    # print('cards1', cards1, '\ncards2', cards2)
    c1, c2 = cards1.pop(0), cards2.pop(0)
    # print('cards', c1, c2, 'lengths', len(cards1), len(cards2))
    if c1 <= len(cards1) and c2 <= len(cards2):
        print('\n------------playing recursion------------')
        cards1_copy = cards1[:c1].copy()
        cards2_copy = cards2[:c2].copy()

        winner1_rec = True
        history_rec = ([(0, 0)], [(0, 0)])
        while cards1_copy != [] and cards2_copy != []:
            c1_rec, c2_rec, winner1_rec = recursion_game(cards1_copy, cards2_copy, history_rec)
            if winner1_rec:
                cards1_copy += [c1_rec, c2_rec]
            else:
                cards2_copy += [c2_rec, c1_rec]
        return c1, c2, winner1_rec
    # print('normal rules', c1, c2, c1 > c2)
    return c1, c2, c1 > c2


if __name__ == '__main__':
    players = read_input_blocks('input')
    cards_1 = [int(p1) for p1 in players[0][1:]]
    cards_2 = [int(p2) for p2 in players[1][1:]]

    history = ([(0, 0)], [(0, 0)])

    while cards_2 != [] and cards_1 != []:
        c1, c2, winner1 = recursion_game(cards_1, cards_2, history)
        # print('\n----------out of recursion', c1, c2, winner1)
        if winner1:
            cards_1 += [c1, c2]
        else:
            cards_2 += [c2, c1]

    winner = cards_1 if len(cards_1) else cards_2
    score = sum([(len(winner) - i) * card for i, card in enumerate(winner)])
    print(score)
