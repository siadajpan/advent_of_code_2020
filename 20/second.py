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
        updates = [(self.position + [-1, 0], 'bottom', self.top), (self.position + [1, 0], 'top', self.bottom),
                   (self.position + [0, -1], 'right', self.left), (self.position + [0, 1], 'left', self.right)]

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
        space.update(**{name: picture})

    first_name = list(space.keys())[8]
    # print(space[list(space.keys())[0]])
    tiles_left = space.copy()
    first_pic = space[first_name]
    # first_name, first_pic = corners[0]
    corner_tile.tile_name = first_name
    neighbours_update = corner_tile.update_picture(first_pic)
    tiles_left.pop(first_name)

    for _ in range(1000):
        update_neighbours(neighbours_update, tiles)
        # print('updaqted neighbours', tiles)
        old_update = neighbours_update.copy()
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
                neighbours_update = tile.update_picture(pic_passing)
                tile.tile_name = name_passing
                tiles_left.pop(name_passing)

        if np.array_equal(np.array(neighbours_update), np.array(old_update)):
            break
        print(len(tiles_left))

    print(tiles)
    positions = sorted([(i, tile.position) for i, tile in enumerate(tiles)],
                       key=lambda x: x[1][0] * 10000 + x[1][1])
    print(positions)
    print(tiles[7].picture, '\n', tiles[3].picture, '\n', tiles[0].picture)