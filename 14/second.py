import re
import struct

from utils.utils import read_input, read_input_ex

def apply_mask(mask, row):
    out = []
    for el_m, el_r in zip(mask, row):
        out.append(el_r) if el_m == '0' else out.append(el_m)

    return ''.join(out)

def update_memory(memory, mask, value):
    if 'X' in mask:
        x_index = mask.index('X')
        mask_0 = f'{mask[:x_index]}0{mask[x_index+1:]}'
        update_memory(memory, mask_0, value)
        mask_1 = f'{mask[:x_index]}1{mask[x_index+1:]}'
        update_memory(memory, mask_1, value)
    else:
        # address = str(int(mask, 2))
        memory.update(**{mask: value})


if __name__ == '__main__':
    data = read_input(__file__)
    # print(data)
    mask = {}
    out_number = {}
    for row in data:
        comm, _, number = row.split(' ')
        if comm == 'mask':
            mask = number
            print(mask)
        elif 'mem' in comm:
            memory_loc = re.match(r'mem\[(\d+)\]', comm).group(1)
            memory_loc = f'{int(memory_loc):#038b}'[2:]
            mask = apply_mask(mask, memory_loc)
            update_memory(out_number, mask, int(number))
            # print(code)
            # code = apply_mask(mask, code)
            # print(code)
            # print(int(code, 2))
            # out_number.update(**{memory_loc: int(code, 2)})
    print(out_number)
    print(sum(out_number.values()))
