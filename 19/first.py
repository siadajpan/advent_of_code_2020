import re
from functools import lru_cache

import numpy as np

from utils.utils import read_input_blocks


def parse_rule(rule):
    key, value = re.match(r'(\d+): (.*)', rule).groups()
    only_digits = re.match('([\d+\s*]+)$', value)
    if only_digits:
        return key, ('strict', np.array(only_digits.group(1).split(), dtype=int))
    digits_with_or = re.match(r'([\d+\s*]+)\|([\d+\s*]+)', value)
    if digits_with_or:
        return key, ('or', np.array([np.array(v.split(), dtype=int)
                              for v in digits_with_or.groups()], dtype=int))
    letters_only = re.match(r'"(\w+)"$', str(value))
    if letters_only:
        return key, ('letter', letters_only.group(1))
    raise NotImplementedError('wrong rule')


def add_regex(rule, regex, rules_dict):
    name, rule_val = rule
    if name == 'letters':
        return rule_val
    elif name == 'strict':
        addition = ''
        for val in rule_val:
            subrule = rules_dict[val]
            addition += add_regex(subrule, regex, rules_dict)
        return addition
    print(rule)



def check_pass(dict, text, match_code):
    pass


if __name__ == '__main__':
    data = read_input_blocks('input_ex')
    print(data)

    rules, checks = data
    rules_dict = {}
    for rule in rules:
        key, value = parse_rule(rule)
        rules_dict.update(**{key: value})

    print(rules_dict)
    # print(extend_rule(rules_dict['0'], rules_dict))
    # [rules.update(**{key: value}) for key, value in
    # print(rules)

    # [[4 1 5]]
    # if len == 1:
    #     for i in els:
    #         text, 4, 1, 5
