import os

import numpy as np


def read_input(input_path: str = 'input', type_: type = str):
    with open(input_path) as file:
        rows = file.read()[:-1].split('\n')

        return np.asarray(rows, dtype=type_)


def read_input_blocks(file: str = 'input', join: str = None):
    elements = read_input(file)

    new_block = []
    blocks = []
    for el in elements:
        if el == '':
            blocks.append(new_block)
            new_block = []
            continue
        new_block.append(el)

    blocks.append(new_block)

    if join is None:
        return blocks

    out = []
    for el in blocks:
        out.append(join.join(el))

    return out
