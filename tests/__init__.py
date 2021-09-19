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
    # print(item.magic_mods_index)
    # item.print_data(item.magic_mods_index)
    # item.change_max_durability(80)
    # item.clear_magic_mods()
    # item.update_id(123456)
    # item.change_rarity(get_dict_key_from_value(RARITIES, 'unique'))
    # item.change_type_code('&90 ')
    # item.change_level(127)
    item.edit(index=rarity_details['index'], data=list(reversed(dec_to_bin(1434 + 1, length=15))))
    # item.insert(index=item.magic_mods_index + 40, data=list('1111001111'))
    # item.delete_data(index=item.magic_mods_index, length=10)
    # 10101000011000000000111010000110000000001111100101100000000111111111
    # item.edit(index=item.magic_mods_index, data=list(reversed(
    #     dec_to_bin(
    #         360 + 1,
    #         length=9
    #     )
    # )))

    # 1100101000011000

    # item.add_magic_mod(
    #     mod_id=get_mod_id_by_code('poison_len_reduced_by_%'), values=dict(value=25)
    # )


char.save(
    file_path,
)

