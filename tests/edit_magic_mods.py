import os

from src.models.character import Character
from src.common.utils import dec_to_bin, get_mod_id_by_code
from src.common.constants.item import RARITIES

file_dir = 'C:\\Users\\tring\\AppData\\Roaming\\MedianXL\\save'
backup_dir = 'C:\\Users\\tring\\AppData\\Roaming\\MedianXL\\save\\backups'

file_name = 'Shin.d2s'

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
    # item.clear_magic_mods()

    for mod_data in [
        # dict(mod_id=get_mod_id_by_code('+_all_skill_level'), from_values={'value': 1}, to_values={'value': 2}),
        # dict(mod_id=get_mod_id_by_code('+_class_skill_level'), from_values={'class_id': 4, 'skill_level': 1}, to_values={'class_id': 4, 'skill_level': 2}),

        # dict(mod_id=get_mod_id_by_code('+%_movement_speed'), from_values={'value': 25}, to_values={'value': 40}),
        # dict(mod_id=get_mod_id_by_code('+%_cast_speed'), from_values={'value': 23}, to_values={'value': 30}),
        # dict(mod_id=get_mod_id_by_code('+%_block_speed'), from_values={'value': 32}, to_values={'value': 40}),

        dict(mod_id=get_mod_id_by_code('+_strength'), from_values={'value': 126}, to_values={'value': 140}),
        dict(mod_id=get_mod_id_by_code('+_dexterity'), from_values={'value': 126}, to_values={'value': 140}),
        dict(mod_id=get_mod_id_by_code('+_vitality'), from_values={'value': 126}, to_values={'value': 140}),
        dict(mod_id=get_mod_id_by_code('+_energy'), from_values={'value': 126}, to_values={'value': 140}),

        # dict(mod_id=get_mod_id_by_code('+%_strength'), from_values={'value': 7}, to_values={'value': 10}),
        # dict(mod_id=get_mod_id_by_code('+%_dexterity'), from_values={'value': 7}, to_values={'value': 10}),
        # dict(mod_id=get_mod_id_by_code('+%_vitality'), from_values={'value': 7}, to_values={'value': 10}),
        # dict(mod_id=get_mod_id_by_code('+%_energy'), from_values={'value': 7}, to_values={'value': 10}),

        # dict(mod_id=get_mod_id_by_code('+%_dexterity'), from_values={'value': 22}, to_values={'value': 25}),

        # dict(mod_id=get_mod_id_by_code('+%_enhanced_defense'), from_values={'value': 106}, to_values={'value': 150}),
        # dict(mod_id=get_mod_id_by_code('+%_enhanced_dmg'), from_values={'min_dmg': 152, 'max_dmg': 200}, to_values={'min_dmg': 200, 'max_dmg': 200}),

        # dict(mod_id=get_mod_id_by_code('+%_phy_mag_spell_dmg'), from_values={'value': 8}, to_values={'value': 10}),
        # dict(mod_id=get_mod_id_by_code('+%_fire_spell_dmg'), from_values={'value': 8}, to_values={'value': 10}),
        # dict(mod_id=get_mod_id_by_code('+%_cold_spell_dmg'), from_values={'value': 8}, to_values={'value': 10}),
        # dict(mod_id=get_mod_id_by_code('+%_lightning_spell_dmg'), from_values={'value': 8}, to_values={'value': 10}),
        # dict(mod_id=get_mod_id_by_code('+%_poison_spell_dmg'), from_values={'value': 8}, to_values={'value': 10}),

        # dict(mod_id=get_mod_id_by_code('+_spell_focus'), from_values={'value': 40}, to_values={'value': 55})
    ]:
        item.edit_magic_mod(
            **mod_data
        )

char.save(
    file_path,
)
