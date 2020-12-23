MAX_CUP = 1000000


# MAX_CUP = 9


class Cup:
    def __init__(self, number):
        self.number = number
        self.next_cup = None
        self.picked = False

    def update_next_cup(self, next_cup):
        self.next_cup = next_cup

    def __repr__(self):
        return f'(Cup: {self.number} next one: {self.next_cup.number})'


def play(current_cup, cups):
    cup_picked = [current.next_cup]
    for i in range(2):
        cup_picked.append(cup_picked[-1].next_cup)
    for cup in cup_picked:
        cup.picked = True

    current_cup.next_cup = cup_picked[-1].next_cup
    current_number = current.number - 1 if current.number > 1 else MAX_CUP
    while cups[str(current_number)].picked:
        current_number = current_number - 1 if current_number > 1 else MAX_CUP

    target = cups[str(current_number)]
    cup_picked[-1].next_cup = target.next_cup
    target.next_cup = cup_picked[0]
    for cup in cup_picked:
        cup.picked = False

    return current_cup.next_cup


def print_cups(cups):
    current = cups['1']
    out = []
    for i in range(9):
        out.append(current.number)
        current = current.next_cup
    print(out)


if __name__ == '__main__':
    # cups = '389125467'
    cups = '368195742'
    cups = [int(n) for n in list(cups)] + [i for i in range(10, MAX_CUP + 1)]
    max_number = max(cups)

    cups = {str(number): Cup(number) for number in cups}
    cups_names = list(cups.keys())
    for cup, next_cup in zip(cups_names, [*cups_names[1:], cups_names[0]]):
        cups[cup].update_next_cup(cups[next_cup])
    print_cups(cups)

    current = cups[cups_names[0]]
    for i in range(10000000):
        current = play(current, cups)

    after_1 = cups['1'].next_cup
    print(after_1)
    after_2 = after_1.next_cup
    print(after_2)
    print('result', after_1.number * after_2.number)
