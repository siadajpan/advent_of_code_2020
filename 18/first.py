import re

from utils.utils import read_input


def find_solution(text):
    # find inner parenthesis
    inner = re.match(r'.*\(([^()]+)\).*', text)
    if inner:
        inner_par = inner.group(1)
        inner_solution = eval_solution(inner_par)
        text = text.replace(f'({inner_par})', str(inner_solution))
        return find_solution(text)
    else:
        out = eval_solution(text)
        return out


def eval_solution(text):
    first, rest = re.match(r'(\d+ [+*] \d+)\s*(.*)', text).groups()
    result = eval(first)
    if rest:
        return eval_solution(f'{result} {rest}')
    else:
        return result


if __name__ == '__main__':
    data = read_input('input')
    print(sum([find_solution(d) for d in data]))
