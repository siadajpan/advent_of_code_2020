import numpy as np

if __name__ == '__main__':
    # data_ex = '389125467'
    cups = '368195742'

    def play(data):
        current, picked = data[0], data[1:4]
        data = data[4:] + [current]
        current = (current-1 if current > 0 else current-1+max(data))
        while current not in data:
            current = (current-1 if current > 0 else current+max(data))
        else:
            for x in reversed(picked):
                data.insert(data.index(current)+1, x)
        return data


    cups = [int(x) for x in cups]
    for x in range(100):
        cups = play(cups)
    print(''.join(str(a) for a in cups[cups.index(1):] + cups[:cups.index(1)]))