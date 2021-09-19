import os
from itertools import zip_longest

from config import ROOT_PATH
from src.common.constants.modifies import MODIFIES


def dec_to_bin(value: int,
               length: int = None,
               padding: str = None):
    if not padding:
        padding = '0'

    if not length:
        length = 2

    template = '{:' + '{padding}{length}b'.format(
        padding=padding,
        length=length
    ) + '}'
    return template.format(value)


def bin_to_dec(data: str) -> int:
    result = int(data, 2)
    return result


def dec_to_hex(number: int,
               length: int = None,
               padding: str = None) -> str:
    if not length:
        length = 2

    if not padding:
        padding = '0'

    template = '{:' + '{padding}{length}x'.format(
        padding=padding,
        length=length
    ) + '}'

    result = template.format(number)

    if len(result) % 2:
        result = padding + result

    return result


def bin_to_hex(data: str,
               length: int = None,
               padding: str = None):
    if not padding:
        padding = '0'

    dec = bin_to_dec(data)

    result = dec_to_hex(dec, length=length, padding=padding)

    return result


def split_array(array, n, padding=None):
    return zip_longest(*[iter(array)] * n, fillvalue=padding)


def make_byte_array_from_hex(data):
    return [
        dec_to_hex(b)
        for b in bytearray.fromhex(data)
    ]


def make_d2s_file_path(file_name: str, *paths):
    target = os.path.join(ROOT_PATH, 'd2s_files')

    for p in paths:
        target = os.path.join(target, p)

    if not os.path.exists(target):
        os.makedirs(target)

    if not file_name.endswith('.d2s'):
        file_name = file_name + '.d2s'

    return os.path.join(target, file_name)


def get_dict_key_from_value(data: dict, value: any):
    result = None

    for k, v in data.items():
        if v == value:
            result = k
            break
    return result


def get_mod_id_by_code(code):
    result = None
    for k, v in MODIFIES.items():
        if v['code'] == code:
            result = k
            break
    return result
