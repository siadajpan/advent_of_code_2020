import re

from utils.utils import read_input_blocks


def parse_rule(rule, second: bool):
    key, value = re.match(r'(\d+): (.*)', rule).groups()
    if second and key == '8':
        return key, f'({value})+'
    elif second and key == '11':
        # return 11 42 31
        # print('got 11', value.split())
        return key, '((42) (31))'
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
    second = True
    rules, checks = data

    rules_dict = {}
    for rule in rules:
        # elif second and rule == '11: 42 31':
        #     rule = '11: 42 31 | 42 11 31'
        key, value = parse_rule(rule, second)
        rules_dict.update(**{key: value})

    # print(rules_dict['31'])
    extended = extend_rule(rules_dict['0'], rules_dict)
    extended = ''.join(extended).replace('[', '(').replace(']', ')').replace(' ', '')
    print(sum([(re.fullmatch(extended, name) is not None) for name in checks]))
