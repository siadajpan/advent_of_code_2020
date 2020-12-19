import re

from utils.utils import read_input_blocks


def parse_rule(rule):
    key, value = re.match(r'(\d+): (.*)', rule).groups()
    only_digits = re.match('([\d+\s*]+)$', value)
    if only_digits:
        return key, (only_digits.group(1))
    digits_with_or = re.match(r'([\d+\s*]+)\|([\d+\s*]+)', value)
    if digits_with_or:
        regex = f'(({digits_with_or.group(1)})|({digits_with_or.group(2)}))'
        return key, regex
    letters_only = re.match(r'"(\w+)"$', str(value))
    if letters_only:
        return key, letters_only.group(1)
    raise NotImplementedError('wrong rule')


def extend_rule(rule, rules_dict):
    rule = str(rule).replace('\n', '')
    eights = 0
    elevens = 0
    for _ in range(1500):
        match_iter = re.finditer(r'(\d+)', rule)
        try:
            match = next(match_iter)
            # print(match)
            # if match.group(0) == '8':
            #     print('eight')
            #     eights += 1
            #     match = next(match_iter)
            rule = f'{rule[:match.start(0)]} {rules_dict[match.group(0)]} {rule[match.end(0):]}'
            # print('rule', rule)
        except StopIteration:
            break

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
    # print(extended)
    extended = ''.join(extended).replace('[', '(').replace(']', ')').replace(' ', '')
    print(sum([(re.fullmatch(extended, name) is not None) for name in checks]))
