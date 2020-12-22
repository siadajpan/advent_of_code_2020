import re

import numpy as np

from utils.utils import read_input_blocks


def parse_limits(limit):
    name, l1l, l1h, l2l, l2h = re.match(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)', limit).groups()
    return name, [(int(l1l), int(l1h)), (int(l2l), int(l2h))]


def check_limit(number, limits):
    for l_low, l_high in limits:
        if l_low <= number <= l_high:
            return True

    return False


def parse_nearby_ticket(ticket):
    return np.array(ticket.split(','), dtype=int)


if __name__ == '__main__':
    locations, my_ticket, nearby = read_input_blocks('input')

    all_limits = [parse_limits(l) for l in locations]
    nearby_tickets = [parse_nearby_ticket(ticket) for ticket in nearby[1:]]
    print(nearby_tickets[0])
    invalidity = 0
    for ticket in nearby_tickets:
        for el in ticket:
            if not any([check_limit(el, l) for name, l in all_limits]):
                invalidity += el
                print(ticket, el)
                # break
        # if invalidity:
        #     break
    # print(nearby[0])
    print(invalidity)
