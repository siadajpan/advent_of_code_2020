import numpy as np

from utils.utils import read_input


def find_neighbours(cut):
    neighbours = np.sum(cut) - cut[1, 1, 1]
    # if neighbours:
    #     print(cut, '\nfound:', neighbours)
    return neighbours


if __name__ == '__main__':
    sim_length = 7
    data = read_input()
    old_size = len(data)
    data = np.array([list(d.replace('.', '0').replace('#', '1')) for d in data], dtype=int)
    old_h, old_w = data.shape
    new_size = np.array(data.shape) + sim_length*2
    new_mid = np.zeros(new_size, dtype=int)
    new_mid[sim_length: sim_length + old_w, sim_length: sim_length + old_h] = data
    space = np.zeros((sim_length * 2 + 1, *new_size), dtype=int)
    space[sim_length] = new_mid
    xm, ym, zm = space.shape
    # print(new_mid)
    # print(space)

    for _ in range(sim_length-1):
        new_space = space.copy()
        for x in range(1, xm-1):
            for y in range (1, ym-1):
                for z in range(1, zm-1):
                    cut = new_space[x-1:x+2, y-1:y+2, z-1:z+2]
                    if new_space[x, y, z] and not find_neighbours(cut) in [2, 3]:
                        space[x, y, z] = 0
                    if not new_space[x, y, z] and find_neighbours(cut) == 3:
                        # print('x y z', x, y, z)
                        space[x, y, z] = 1
        print('--------------\n', space)
    print(np.sum(space))
    # data[data == '.'] = 0
    # data[data == '#'] = 1

    # space = np.zeros((new_size, ) * 3, dtype=int)
    # space[np.where(data == '#')] = 1
    # space[sim_length: sim_length + old_size, sim_length: sim_length + old_size, sim_length: sim_length + old_size] =
    # space
    # print(space)
