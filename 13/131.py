import math
import re
from functools import lru_cache

import numpy as np

from utils.utils import read_input


def get_lcm(n1,n2):
    #find gcd
    gcd = math.gcd(n1,n2)

    #formula
    result = int((n1*n2)/gcd)
    return result

def find_lcm_arr(numbers):
    if len(numbers) == 1:
        return numbers[0]

    if len(numbers) == 2:
        return get_lcm(*numbers)

    lcm = numbers[0]
    for number in numbers[1:]:
        lcm = get_lcm(lcm, number)

    return lcm

if __name__ == '__main__':
    data = read_input()
    print(data)
    timestamp, buses = data
    buses_with_x = buses.split(',')
    print(buses_with_x)
    timestamp = int(timestamp)
    buses = re.split(r'\D+', buses)
    bus_indexes = [buses_with_x.index(bus) for bus in buses]
    buses = np.array(buses, dtype=int)
    print(bus_indexes)
    print(timestamp, buses)

    max_bus_index = np.argmax(buses)
    max_bus = buses[max_bus_index]
    start_offset = bus_indexes[max_bus_index]

    timestamp = max_bus - start_offset

    for i in range(100):
        subsequent = [(timestamp + bus_indexes[i]) % bus == 0 for i, bus in enumerate(buses)]
        if all(subsequent):
            print('Found', timestamp)
            break

        timestamp += find_lcm_arr(buses[subsequent])
