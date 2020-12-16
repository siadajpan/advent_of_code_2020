import re

import numpy as np

from utils.utils import read_input_blocks


def parse_limits(limit):
    name, l1l, l1h, l2l, l2h = re.match(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)', limit).groups()
    return name, [(int(l1l), int(l1h)), (int(l2l), int(l2h))]


def check_limit(number, limits):
    # print('checking limit', limits, number)
    for l_low, l_high in limits:
        if number >= l_low and number <= l_high:
            # print('true')
            return True
    # print('false')
    return False


def check_limit_row(numbers, limits):
    return all([check_limit(number, limits) for number in numbers])


def parse_nearby_ticket(ticket):
    return np.array(ticket.split(','), dtype=int)


if __name__ == '__main__':
    locations, my_ticket, nearby = read_input_blocks('input')

    all_limits = [parse_limits(l) for l in locations]
    nearby_tickets = np.asarray([parse_nearby_ticket(ticket) for ticket in nearby[1:]])
    valid = []
    for ticket in nearby_tickets:
        invalid = False
        for el in ticket:
            if not any([check_limit(el, l) for name, l in all_limits]):
                invalid = True
                break
        if not invalid:
            valid.append(ticket)

    my_ticket = parse_nearby_ticket(my_ticket[1])
    print('my ticket', my_ticket)
    valid = np.asarray(valid)
    print(valid)
    unused_cols = list(range(len(my_ticket)))
    print('unused', unused_cols)
    print(all_limits)
    pairing = {}
    for i in range(100):
        print('unused', unused_cols)
        if len(unused_cols) == 0:
            break

        for col in unused_cols:
            numbers_to_check = valid[:, col]
            print('numbers to check', numbers_to_check)
            limit_passed = np.array([(name, check_limit_row(numbers_to_check, lim)) for name, lim in all_limits])
            print('limits passed', limit_passed)
            limit_pass = limit_passed[:, 1] == 'True'
            if sum(limit_pass) == 1:
                limit = all_limits[list(limit_pass).index(True)]
                print(col, limit[0])
                pairing.update(**{limit[0]: col})
                unused_cols.remove(col)
                all_limits.remove(limit)
                break
            else:
                print('---------------valid for ', sum(limit_pass))

    print(pairing)
    out = 1
    print('my ticket', my_ticket)
    for key, value in pairing.items():
        if 'departure' in key:
            print(key, value, my_ticket[value])
            out *= my_ticket[value]

    print(out)
