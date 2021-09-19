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

    for mod_data in [
        # dict(mod_id=get_mod_id_by_code('+_all_skill_level'), values=dict(value=2)),
        # dict(mod_id=get_mod_id_by_code('+_class_skill_level'), values=dict(class_id=6, skill_level=2)),

        # dict(mod_id=get_mod_id_by_code('+%_block_speed'), values=dict(value=15)),
        # dict(mod_id=get_mod_id_by_code('+%_cast_speed'), values=dict(value=10)),
        # dict(mod_id=get_mod_id_by_code('+%_atk_speed'), values=dict(value=15)),
        # dict(mod_id=get_mod_id_by_code('+%_hit_recovery'), values=dict(value=15)),
        # dict(mod_id=get_mod_id_by_code('+%_movement_speed'), values=dict(value=40)),

        # dict(mod_id=get_mod_id_by_code('+_max_dmg'), values=dict(value=4)),
        # dict(mod_id=get_mod_id_by_code('+_min_dmg'), values=dict(value=114)),

        # dict(mod_id=get_mod_id_by_code('+%_exp_gained'), values=dict(value=1)),
        #
        # dict(mod_id=get_mod_id_by_code('+_defense'), values=dict(value=100)),
        # dict(mod_id=get_mod_id_by_code('+_mana'), values=dict(value=16)),
        # dict(mod_id=get_mod_id_by_code('+_life'), values=dict(value=242)),
        # dict(mod_id=get_mod_id_by_code('+_life_on_melee_atk'), values=dict(value=14)),

        # dict(mod_id=get_mod_id_by_code('+_strength'), values=dict(value=5)),
        # dict(mod_id=get_mod_id_by_code('+_vitality'), values=dict(value=5)),
        # dict(mod_id=get_mod_id_by_code('+_dexterity'), values=dict(value=5)),
        # dict(mod_id=get_mod_id_by_code('+_energy'), values=dict(value=5)),
        #
        # dict(mod_id=get_mod_id_by_code('+%_strength'), values=dict(value=15)),
        # dict(mod_id=get_mod_id_by_code('+%_vitality'), values=dict(value=15)),
        # dict(mod_id=get_mod_id_by_code('+%_dexterity'), values=dict(value=2)),
        # dict(mod_id=get_mod_id_by_code('+%_energy'), values=dict(value=15)),

        # dict(mod_id=get_mod_id_by_code('+_spell_focus'), values=dict(value=40)),
        #
        # dict(mod_id=get_mod_id_by_code('+%_magic_resist'), values=dict(value=2)),
        # dict(mod_id=get_mod_id_by_code('+%_fire_resist'), values=dict(value=35)),
        # dict(mod_id=get_mod_id_by_code('+%_cold_resist'), values=dict(value=5)),
        # dict(mod_id=get_mod_id_by_code('+%_lightning_resist'), values=dict(value=37)),
        # dict(mod_id=get_mod_id_by_code('+%_poison_resist'), values=dict(value=37)),

        # dict(mod_id=get_mod_id_by_code('+%_fire_spell_dmg'), values=dict(value=1)),
        # dict(mod_id=get_mod_id_by_code('+%_cold_spell_dmg'), values=dict(value=12)),
        # dict(mod_id=get_mod_id_by_code('+%_lightning_spell_dmg'), values=dict(value=10)),
        # dict(mod_id=get_mod_id_by_code('+%_poison_spell_dmg'), values=dict(value=10)),
        # dict(mod_id=get_mod_id_by_code('+%_phy_mag_spell_dmg'), values=dict(value=4)),
        # dict(mod_id=get_mod_id_by_code('-%_enemy_fire_resist'), values=dict(value=10)),
        # dict(mod_id=get_mod_id_by_code('-%_enemy_lightning_resist'), values=dict(value=25)),
        # dict(mod_id=get_mod_id_by_code('-%_enemy_poison_resist'), values=dict(value=4)),
        #
        # dict(mod_id=get_mod_id_by_code('+%_enhanced_defense'), values=dict(value=38)),
        #
        dict(mod_id=get_mod_id_by_code('poison_len_reduced_by_%'), values=dict(value=25)),

    ]:
        item.delete_magic_mode(
            **mod_data
        )

char.save(
    file_path,
)

