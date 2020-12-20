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


class Tile:
    def __init__(self, position):
        self.position = position
        self.picture = None
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None
        self.tile_name = None

    def update_picture(self, arr, position):
        self.picture = arr
        self.left, self.right, self.top, self.bottom = get_sides(arr)
        # which tile, which position to update, and the matching side
        updates = [(position + [-1, 0], 'bottom', self.top), (position + [1, 0], 'top', self.bottom),
                   (position + [0, -1], 'right', self.left), (position + [0, 1], 'left', self.right)]
        return updates

    def passed(self):
        return self.picture is not None

    def get_passing(self):
        return self.left, self.right, self.top, self.bottom

    def update_match(self, position_to_update, update):
        if position_to_update == 'bottom':
            self.bottom = update
        elif position_to_update == 'top':
            self.top = update
        elif position_to_update == 'left':
            self.left = update
        elif position_to_update == 'right':
            self.right = update
        else:
            raise ValueError('wrong element to update', position_to_update)

    def check_passing(self, picture):
        l, r, t, b = get_sides(picture)

        mine = [self.left, self.right, self.top, self.bottom]
        rotations = [(l, r, t, b), (l[::-1], r[::-1], t, b), (l, r, t[::-1], b[::-1])]
        rotations = [r[i:] + r[:i] for i in range(4) for r in rotations]
        print('all rot', rotations)
        print('checking\n', '\n'.join(picture), mine)
        for r in rotations:
            passed = True
            for i, ri in enumerate(r):
                if mine[i] == None:
                    continue
                print('passing', i, mine[i], 'with', ri)
                if mine[i] != ri:
                    passed = False
                    break
            if passed:
                print('all passed', mine, r)
                raise NotImplementedError()
                return True, r
        return False, None


def update_neighbours(update, tiles):
    for position, part_to_update, new_side in update:
        for tile in tiles:
            if all(tile.position == position):
                if tile.passed():
                    continue
                tile.update_match(part_to_update, new_side)
                break
        new_tile = Tile(position)
        new_tile.update_match(part_to_update, new_side)
        tiles.append(new_tile)


def tile_passing(picture, tile: Tile):
    if tile.passed():
        raise ValueError('tile already passed')



if __name__ == '__main__':
    data = read_input_blocks('input_ex')
    space = {}
    corner_tile = Tile((0, 0))
    tiles = [corner_tile]

    for block in data:
        name, picture = parse_block(block)
        blocks = space.update(**{name: picture})

    tiles_left = space.copy()

    corners = []
    for tile, pic in space.items():
        # print('t', tile, pic)
        # print('sides', get_sides(pic))
        empty_sides = 0
        for side in get_sides(pic):
            other_sides = get_all_sides_except(space, tile)
            if side not in other_sides and side[::-1] not in other_sides:
                empty_sides += 1
                if empty_sides == 2:
                    corners.append((tile, pic))

    first_name, first_pic = corners[0]
    corner_tile.tile_name = first_name
    neighbours_update = corner_tile.update_picture(first_pic, np.array([0, 0]))


    for _ in range(100):
        update_neighbours(neighbours_update, tiles)
        for tile in tiles:
            new_passing = 0
            if tile.passed():
                continue
            for tile_left, pic_left in tiles_left.items():
                passed = tile.check_passing(pic_left)

