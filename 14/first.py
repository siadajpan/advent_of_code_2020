import re

from utils.utils import read_input


def apply_mask(mask, row):
    out = []
    for el_m, el_r in zip(mask, row):
        out.append(el_r) if el_m == 'X' else out.append(el_m)
    return ''.join(out)


if __name__ == '__main__':
    data = read_input()
    mask = {}
    out_number = {}
    for row in data:
        comm, _, number = row.split(' ')
        if comm == 'mask':
            mask = number
            print(mask)
        elif 'mem' in comm:
            memory_loc = re.match(r'mem\[(\d+)\]', comm).group(1)
            code = f'{int(number):#038b}'[2:]
            print(code)
            code = apply_mask(mask, code)
            print(code)
            print(int(code, 2))
            out_number.update(**{memory_loc: int(code, 2)})
    print(out_number)
    print(sum(out_number.values()))
