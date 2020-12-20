import re

from utils.utils import read_input_blocks


def parse_rule(rule):
    key, value = re.match(r'(\d+): (.*)', rule).groups()

    return key, f'({value})'.replace('"', '')


def extend_rule(rule, rules_dict):
    rule = str(rule).replace('\n', '')
    for _ in range(10000):
        match = re.search(r'(\d+)', rule)
        if not match:
            break

        rule = f'{rule[:match.start(0)]} {rules_dict[match.group(0)]} {rule[match.end(0):]}'

    return rule


if __name__ == '__main__':
    data = read_input_blocks('input')
    second = False
    rules, checks = data

    rules_dict = {}
    for rule in rules:
        if second and rule == '8: 42':
            rule = '8: 42 | 42 8'
        elif second and rule == '11: 42 31':
            rule = '11: 42 31 | 42 11 31'
        key, value = parse_rule(rule)
        rules_dict.update(**{key: value})

    extended = extend_rule(rules_dict['0'], rules_dict)
    extended = ''.join(extended).replace('[', '(').replace(']', ')').replace(' ', '')
    print(sum([(re.fullmatch(extended, name) is not None) for name in checks]))
