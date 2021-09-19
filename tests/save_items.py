import os

from src.models.character import Character
from src.common.utils import make_d2s_file_path

file_dir = 'C:\\Users\\tring\\AppData\\Roaming\\MedianXL\\save'

file_name = 'Shin.d2s'

origin_file_path = os.path.join(file_dir, file_name)
with open(origin_file_path, 'rb') as file_ref:
    file_data = file_ref.read()

char = Character(file_data.hex())
for item in char.items:
    if item.panel != 'horadric_cube':
        continue
    print(''.join(item.bin_data))
    print(
        f'(location: {item.location})',
        f'(panel: {item.panel})',
        f'(equipped_location: {item.equipped_location})',
        f'(type_code: {item.type_code})',
        f'(rarity: {item.rarity})',
        f'(has_class_spec: {item.has_class_spec})',
    )
    item.save(make_d2s_file_path(
        "Ghost Trance", 'etc'
    ))

# ['4a', '4d', '10', '00', 'a2', '00', '65', '00', '68', '82', '06', '17', '03', '02']
# 100101001 00110100

# char.save(os.path.join(edited_dir, file_name))
