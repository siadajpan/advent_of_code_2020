import re
import struct

import numpy as np

from utils.utils import read_input

if __name__ == '__main__':
    data = read_input()
    print(data)
    timestamp, buses = data
    timestamp = int(timestamp)
    buses = np.array(re.split(r'\D+', buses), dtype=int)
    print(timestamp, buses)
    next_bus = min([(buses[i], bus - timestamp % bus) for i, bus in enumerate(buses)], key=lambda x: x[1])
    print(next_bus, next_bus[0] * next_bus[1])
