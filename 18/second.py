import re

from utils.utils import read_input


class A:
    # class where multiplying is adding and adding is multiplying
    def __init__(self, number):
        self.n = int(number)

    def __add__(self, other):
        return A(other.n * self.n)

    def __mul__(self, other):
        return A(other.n + self.n)


if __name__ == '__main__':
    data = read_input('input')
    # change + for * and * for +
    replaced = [line.replace('+', '^').replace('*', '+').replace('^', '*') for line in data]
    # change all numbers for A(number)
    with_classes = [re.sub(r'(\d+)', r'A(\1)', a_) for a_ in replaced]
    # evaluate all
    print(sum([eval(a_).n for a_ in with_classes]))
