MODIFY_ID_LENGTH = 9

MODIFIES = {
    0: {
        'code': '+_strength',
        'length': 11,
        'struct': [
            {
                'length': 11,
                'min_value': -200,
                'code': 'value'
            }
        ]
    },
    1: {
        'code': '+_energy',
        'length': 11,
        'struct': [
            {
                'length': 11,
                'min_value': -200,
                'code': 'value'
            }
        ]
    },
    2: {
        'code': '+_dexterity',
        'length': 11,
        'struct': [
            {
                'length': 11,
                'min_value': -200,
                'code': 'value'
            }
        ]
    },
    3: {
        'code': '+_vitality',
        'length': 11,
        'struct': [
            {
                'length': 11,
                'min_value': -200,
                'code': 'value'
            }
        ]
    },
    7: {
        'code': '+_life',
        'length': 12,
        'struct': [
            {
                'length': 12,
                'min_value': -500,
                'code': 'value'
            }
        ]
    },
    9: {
        'code': '+_mana',
        'length': 12,
        'struct': [
            {
                'length': 12,
                'min_value': -500,
                'code': 'value'
            }
        ]
    },
    16: {
        'code': '+%_enhanced_defense',
        'length': 10,
        'struct': [
            {
                'length': 10,
                'min_value': -823,
                'code': 'value'
            }
        ]
    },
    17: {
        'code': '+%_enhanced_dmg',
        'length': 20,
        'struct': [
            {
                'length': 10,
                'min_value': -823,
                'code': 'max_dmg'
            },
            {
                'length': 10,
                'min_value': -823,
                'code': 'min_dmg'
            },
        ]
    },
    21: {
        'code': '+_min_dmg',
        'length': 50,
        'struct': [
            {
                'length': 11,
                'min_value': 0,
                'code': 'value'
            },
            {
                'length': 39,
                'code': 'meta'
            }
        ]
    },
    22: {
        'code': '+_max_dmg',
        'length': 50,
        'struct': [
            {
                'length': 11,
                'min_value': 0,
                'code': 'value'
            },
            {
                'length': 39,
                'code': 'meta'
            }
        ]
    },
    31: {
        'code': '+_defense',
        'length': 16,
        'struct': [
            {
                'length': 16,
                'min_value': -500,
                'code': 'value'
            }
        ]
    },
    36: {
        'code': '+%_phy_resist',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    37: {
        'code': '+%_magic_resist',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    39: {
        'code': '+%_fire_resist',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    41: {
        'code': '+%_lightning_resist',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    43: {
        'code': '+%_cold_resist',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    45: {
        'code': '+%_poison_resist',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    74: {
        'code': '+_life_gen_per_sec',
        'length': 14,
        'struct': [
            {
                'length': 14,
                'min_value': -1000,
                'code': 'value'
            }
        ]
    },
    79: {
        'code': '+%_gold_find',
        'length': 9,
        'struct': [
            {
                'length': 9,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    80: {
        'code': '+%_magic_find',
        'length': 9,
        'struct': [
            {
                'length': 9,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    83: {
        'code': '+_class_skill_level',
        'length': 7,
        'struct': [
            {
                'length': 3,
                'min_value': 0,
                'code': 'class_id'
            },
            {
                'length': 4,
                'min_value': 0,
                'code': 'skill_level'
            }
        ]
    },
    85: {
        'code': '+%_exp_gained',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -25,
                'code': 'value'
            }
        ]
    },
    91: {
        'code': 'requirements_%',
        'length': 10,
        'struct': [
            {
                'length': 10,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    92: {
        'code': '+_required_lvl',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': 0,
                'code': 'value'
            }
        ]
    },
    93: {
        'code': '+%_atk_speed',
        'length': 9,
        'struct': [
            {
                'length': 9,
                'min_value': -150,
                'code': 'value'
            }
        ]
    },
    96: {
        'code': '+%_movement_speed',
        'length': 9,
        'struct': [
            {
                'length': 9,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    97: {
        'code': 'add_skill',
        'length': 19,
        'struct': [
            {
                'length': 12,
                'min_value': 0,
                'code': 'skill_id'
            },
            {
                'length': 7,
                'min_value': -1,
                'code': 'skill_level'
            }
        ]
    },
    99: {
        'code': '+%_hit_recovery',
        'length': 9,
        'struct': [
            {
                'length': 9,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    102: {
        'code': '+%_block_speed',
        'length': 9,
        'struct': [
            {
                'length': 9,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    105: {
        'code': '+%_cast_speed',
        'length': 9,
        'struct': [
            {
                'length': 9,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    110: {
        'code': 'poison_len_reduced_by_%',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    127: {
        'code': '+_all_skill_level',
        'length': 5,
        'struct': [
            {
                'length': 5,
                'min_value': 0,
                'code': 'value'
            }
        ]
    },
    136: {
        'code': '+%_crushing_blow',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': 0,
                'code': 'value'
            }
        ]
    },
    152: {
        'code': 'indestructible',
        'length': 1,
        'struct': [
            {
                'length': 1,
                'min_value': 0,
                'code': 'value'
            }
        ]
    },
    210: {
        'code': '+_life_on_melee_atk',
        'length': 10,
        'struct': [
            {
                'length': 10,
                'min_value': 0,
                'code': 'value'
            }
        ]
    },
    329: {
        'code': '+%_fire_spell_dmg',
        'length': 10,
        'struct': [
            {
                'length': 10,
                'min_value': -200,
                'code': 'value'
            }
        ]
    },
    330: {
        'code': '+%_lightning_spell_dmg',
        'length': 10,
        'struct': [
            {
                'length': 10,
                'min_value': -200,
                'code': 'value'
            }
        ]
    },
    331: {
        'code': '+%_cold_spell_dmg',
        'length': 10,
        'struct': [
            {
                'length': 10,
                'min_value': -200,
                'code': 'value'
            }
        ]
    },
    332: {
        'code': '+%_poison_spell_dmg',
        'length': 10,
        'struct': [
            {
                'length': 10,
                'min_value': -200,
                'code': 'value'
            }
        ]
    },
    333: {
        'code': '-%_enemy_fire_resist',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    334: {
        'code': '-%_enemy_lightning_resist',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    335: {
        'code': '-%_enemy_cold_resist',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    336: {
        'code': '-%_enemy_poison_resist',
        'length': 8,
        'struct': [
            {
                'length': 8,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    357: {
        'code': '+%_phy_mag_spell_dmg',
        'length': 10,
        'struct': [
            {
                'length': 10,
                'min_value': -200,
                'code': 'value'
            }
        ]
    },
    359: {
        'code': '+%_strength',
        'length': 9,
        'struct': [
            {
                'length': 9,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    360: {
        'code': '+%_dexterity',
        'length': 9,
        'struct': [
            {
                'length': 9,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    361: {
        'code': '+%_energy',
        'length': 9,
        'struct': [
            {
                'length': 9,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    362: {
        'code': '+%_vitality',
        'length': 9,
        'struct': [
            {
                'length': 9,
                'min_value': -100,
                'code': 'value'
            }
        ]
    },
    485: {
        'code': '+_spell_focus',
        'length': 10,
        'struct': [
            {
                'length': 10,
                'min_value': -200,
                'code': 'value'
            }
        ]
    }
}
