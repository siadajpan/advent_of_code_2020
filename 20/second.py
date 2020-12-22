import re

import numpy as np

from utils.utils import read_input_blocks


def get_sides(arr: np.array):
    left = arr[:, 0]
    right = arr[:, -1]
    top = arr[0, :]
    bottom = arr[-1, :]

    return left, right, top, bottom


def parse_block(input_block):
    name = re.match(r'Tile (\d+):', input_block[0]).group(1)
    picture = np.asarray(np.asarray([list(line) for line in input_block[1:]]))
    return name, picture


class Tile:
    def __init__(self, position):
        self.position = np.array(position)
        self.picture = None
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None
        self.tile_name = None

    def update_picture(self, arr):
        self.picture = arr
        self.left, self.right, self.top, self.bottom = get_sides(arr)
        # which tile, which position to update, and the matching side
        updates = [(self.position + [-1, 0], 'bottom', self.top),
                   (self.position + [1, 0], 'top', self.bottom),
                   (self.position + [0, -1], 'right', self.left),
                   (self.position + [0, 1], 'left', self.right)]

        return updates

    @property
    def sides(self):
        return [self.left, self.right, self.top, self.bottom]

    def passed(self):
        return self.picture is not None

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

    def check_passing_sides(self, sides):
        # print('check passing', self.sides, sides)
        for m, s in zip(self.sides, sides):
            if m is None:
                continue
            if not np.array_equal(m, s):
                return False
        return True

    def check_passing_picture(self, picture):
        sides = get_sides(picture)
        return self.check_passing_sides(sides)

    def check_passing(self, picture):
        # print('passing\n', picture, get_sides(picture), self.sides)
        for j in range(2):
            for i in range(4):
                picture = np.rot90(picture)
                if self.check_passing_picture(picture):
                    return True, picture
            picture = np.flip(picture, 0)
            # if self.check_passing_picture(picture):
            #     return True, picture

        return False, None

    def __repr__(self):
        return f'\n({self.tile_name}, {self.position}. {str(self.sides)}, {self.passed()})'


def update_neighbours(update, tiles):
    for position, part_to_update, new_side in update:
        # print('updating neighbours', position, part_to_update, new_side)
        tile_already_created = False
        # find tile to update
        for tile in tiles:
            # print(tile.position, position)
            # if the tile already exists
            if np.array_equal(tile.position, position):
                tile_already_created = True
                if tile.passed():
                    break
                tile.update_match(part_to_update, new_side)
                break

        if not tile_already_created:
            new_tile = Tile(position)
            new_tile.update_match(part_to_update, new_side)
            tiles.append(new_tile)


def print_array(array):
    for row in [''.join([a_ if a_ else ' ' for a_ in a]) for a in array]:
        print(row)


def print_tiles(tiles) -> np.array:
    positions = np.asarray([tile.position for tile in tiles])
    min_row, min_col, max_row, max_col = min(positions[:, 0]), min(positions[:, 1]), max(positions[:, 0]), max(positions[:, 1])
    w, h = tiles[0].picture.shape
    arr_out = np.zeros(((max_row - min_row + 1) * h, (max_col - min_col + 1) * w), dtype=str)
    for tile in tiles:
        row, col = tile.position - np.array([min_row, min_col])
        if tile.picture is not None:
            arr_out[row * h: (row + 1) * h, col * w: (col + 1)* w] = tile.picture
        else:
            if tile.left is not None:
                arr_out[row * h: (row + 1) * h, col * w] = tile.left
            if tile.right is not None:
                arr_out[row * h: (row + 1) * h, (col + 1) * w - 1] = tile.right
            if tile.top is not None:
                arr_out[row * h, col * w: (col + 1) * w] = tile.top
            if tile.bottom is not None:
                arr_out[(row + 1) * h - 1, col * w: (col + 1) * w] = tile.bottom
    print_array(arr_out)
    return arr_out[h: (max_row - min_row) * h, w: (max_col - min_col) * w]


if __name__ == '__main__':
    data = read_input_blocks('input_ex')
    space = {}

    for block in data:
        name, picture = parse_block(block)
        space.update(**{name: picture})

    first_tile = Tile((0, 0))
    tiles = [first_tile]
    first_name = list(space.keys())[6]
    # print(space[list(space.keys())[0]])
    tiles_left = space.copy()
    first_tile.tile_name = first_name
    neighbours_update = first_tile.update_picture(space[first_name])
    tiles_left.pop(first_name)

    for _ in range(1000):
        update_neighbours(neighbours_update, tiles)
        neighbours_update = []

        old_len_tiles = len(tiles_left)
        for tile in tiles:
            new_passing = 0
            name_passing = None
            pic_passing = None
            if tile.passed():
                continue
            for tile_left, pic_left in tiles_left.items():
                passed, picture = tile.check_passing(pic_left)
                if passed:
                    new_passing += 1
                    pic_passing = picture
                    name_passing = tile_left
            if new_passing == 1:
                for update in tile.update_picture(pic_passing):
                    neighbours_update.append(update)
                tile.tile_name = name_passing
                tiles_left.pop(name_passing)

        if len(tiles_left) == old_len_tiles:
            break
        print(len(tiles_left), old_len_tiles)

    arr = print_tiles(tiles)
    # positions = sorted([(i, tile.position) for i, tile in enumerate(tiles)],
    #                    key=lambda x: x[1][0] * 10000 + x[1][1])
    # print(positions)
    print(arr.shape)

    # np.array(arr).