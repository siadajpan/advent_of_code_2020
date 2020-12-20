import re

import numpy as np

from utils.utils import read_input_blocks


def get_sides(arr: np.array):
    left = ''.join([a[0] for a in arr])
    right = ''.join([a[-1] for a in arr])
    top = arr[0]
    bottom = arr[-1]

    return left, right, top, bottom


def parse_block(input_block):
    name = re.match(r'Tile (\d+):', input_block[0]).group(1)
    picture = np.asarray(input_block[1:])
    return name, picture


def get_all_sides_except(space, tile_ex):
    out = []
    for tile, pic in space.items():
        if tile_ex == tile:
            continue
        for side in get_sides(pic):
            out.append(side)
    return out



if __name__ == '__main__':
    data = read_input_blocks('input')
    space = {}

    for block in data:
        name, picture = parse_block(block)
        blocks = space.update(**{name: picture})

    corners = 1
    for tile, pic in space.items():
        # print('t', tile, pic)
        # print('sides', get_sides(pic))
        empty_sides = 0
        for side in get_sides(pic):
            other_sides = get_all_sides_except(space, tile)
            if side not in other_sides and side[::-1] not in other_sides:
                empty_sides += 1
                if empty_sides == 2:
                    corners *= int(tile)
    print(corners)