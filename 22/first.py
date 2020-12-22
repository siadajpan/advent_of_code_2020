import numpy as np

from utils.utils import read_input_blocks

if __name__ == '__main__':
    players = read_input_blocks('input_ex')
    cards_1 = [int(p1) for p1 in players[0][1:]]
    cards_2 = [int(p2) for p2 in players[1][1:]]

    while cards_2 != [] and cards_1 != []:
        c1, c2 = cards_1.pop(0), cards_2.pop(0)
        if c1 > c2:
            cards_1 += [c1, c2]
        else:
            cards_2 += [c2, c1]

    winner = cards_1 if len(cards_1) else cards_2
    score = sum([(len(winner) - i) * card for i, card in enumerate(winner)])
    print(score)
