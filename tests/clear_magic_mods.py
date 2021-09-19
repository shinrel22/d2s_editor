import os

from src.models.character import Character
from src.common.utils import dec_to_bin, get_mod_id_by_code
from src.common.constants.item import RARITIES

file_dir = 'C:\\Users\\tring\\AppData\\Roaming\\MedianXL\\save'
backup_dir = 'C:\\Users\\tring\\AppData\\Roaming\\MedianXL\\save\\backups'

file_name = 'Barbarian.d2s'

file_path = os.path.join(file_dir, file_name)
backup_path = os.path.join(backup_dir, file_name)
with open(file_path, 'rb') as file_ref:
    file_data = file_ref.read()

char = Character(file_data.hex())
for item in char.items:
    # if item.id != 123456:
    if item.panel != 'horadric_cube':
        continue
    rarity_details = item.rarity_details

    print(
        f'(location: {item.location})',
        f'(panel: {item.panel})',
        f'(equipped_location: {item.equipped_location})',
        f'(type_code: {item.type_code})',
        f'(level: {item.level})',
        # f'(x_coordinate: {item.x_coordinate})',
        # f'(y_coordinate: {item.y_coordinate})',
        f'(rarity_details: {rarity_details})',
        f'(defense: {item.defense_value})',
        f'(current_durability: {item.current_durability})',
        f'(max_durability: {item.max_durability})',
    )
    item.print_data(offset=item.magic_mods_index)
    item.clear_magic_mods()

char.save(
    file_path,
)

