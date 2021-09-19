import os

from src.models.character import Character
from src.common.utils import get_dict_key_from_value
from src.common.constants.item import LOCATIONS, PANELS, EQUIPPED_LOCATIONS

file_dir = 'C:\\Users\\tring\\AppData\\Roaming\\MedianXL\\save'

file_name = 'Shin.d2s'

file_path = os.path.join(file_dir, file_name)
with open(file_path, 'rb') as file_ref:
    file_data = file_ref.read()

char = Character(file_data.hex())
x = 0
y = 0
for i in range(10):
    char.add_item_from_file(
        file_path="D:\Documents\d2s_editor\d2s_files\\etc\\Belladonna Extract.d2s",
        location=get_dict_key_from_value(LOCATIONS, 'stored'),
        panel=get_dict_key_from_value(PANELS, 'horadric_cube'),
        x=x,
        y=y
    )
    x += 1
    if x > 14:
        x = 0
        y += 1


# ['4a', '4d', '10', '00', 'a2', '00', '65', '00', '68', '82', '06', '17', '03', '02']
# 100101001 00110100

char.save(file_path)
