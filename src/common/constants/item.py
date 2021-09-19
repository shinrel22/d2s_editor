"""
After this come N items. Each item starts with a basic 14-byte structure.
Many fields in this structure are not "byte-aligned" and are described by their BIT position and sizes.
"""
BASE_STRUCTURE = {
    'header': (0, 16),
    'unknown_1': (16, 4),
    'is_identified': (20, 1),
    'unknown_2': (21, 6),
    'is_socketed': (27, 1),
    'unknown_3': (28, 1),
    'is_picked_up_since_last_save': (29, 1),
    'unknown_4': (30, 2),
    'is_ear': (32, 1),
    'is_starter_gear': (33, 1),
    'unknown_5': (34, 3),
    'is_simple': (37, 1),
    'is_ethereal': (38, 1),
    'unknown_6': (39, 1),
    'is_personalized': (40, 1),
    'unknown_7': (41, 1),
    'is_runeword': (42, 1),
    'unknown_8': (43, 15),
    'location': (58, 3),
    'equipped_location': (61, 4),
    'x_coordinate': (65, 4),
    'y_coordinate': (69, 4),
    'panel': (73, 3),
}

EAR_STRUCTURE = {
    **BASE_STRUCTURE,
    'owner_class': (76, 3),
    'owner_level': (79, 7),

    # Name of the ear's former owner as a null-terminated string.
    # Each character is 7 bits wide, up to a maximum of 15 characters.
    'owner_name': (86, None),
}

NON_EAR_STRUCTURE = {
    **BASE_STRUCTURE,
    # Item type code as 4 8-bit-wide characters,
    # where a space character (0x20) should be treated as a null terminator.
    # Note: Item codes can be 4 characters long.
    'type_code': (76, 32),

    # if item is simple, then it ends here.

    'sockets': (108, 3),

    'unique_id': (111, 32),

    # item level
    'level': (143, 7),

    # Item rarity
    'rarity': (150, 4),

    # From here on out,
    # bit offsets begin to vary depending on the values of the fields, so they will no longer be shown.

    'has_custom_graphic': (154, 1),

    # Only exists when the item has_custom_graphic
    'custom_graphic': (None, 3),

    'has_class_spec': (None, 1),

    # Only exists when the item has_class_spec
    'class_spec': (None, 11),

    # Only exists when the item's rarity is low quality
    'low_quality_id': (None, 3),

    # Only exists when the item's rarity is superior/high quality
    'superior_quality_id': (None, 3),

    # Only exists when the item's rarity is magic
    'magic_pf_type_id': (None, 11),
    'magic_sf_type_id': (None, 11),

    # Only exists when the item's rarity is set
    'set_quality_id': (None, 15),

    # Only exists when the item's rarity is unique
    'unique_quality_id': (None, 15),

    # Only exists when the item's rarity is rare or crafted
    'cr_pf_type_id': (None, 8),
    'cr_sf_type_id': (None, 8),
    # Rare/crafted affixes.
    # Each affix has a 1-bit-wide field denoting whether or not an 11-bit-wide affix ID field follows (`hasAffix`).
    # If `hasAffix` is 1, then an 11-bit-wide field containing the ID of the affix follows.
    # Otherwise, another 1-bit-wide `hasAffix` field follows.
    # There are a total of 6 of these affixes,
    # where the affixes switch off between prefixes and suffixes, starting with prefix.
    'cr_affixes': (None, (6, 6 + (11 * 6))),

    # Only exists when the item has a runeword given to it
    # 12-bit-wide field followed by 4 unknown bits.
    # The 12-bit-wide field is some sort of index into Diablo II's localization string table that
    # contains the name of the runeword of the item,
    # used only for displaying the runeword name of the item.
    # Note: this should not be used to determine what runeword an item is,
    # and instead that should be determined by the order of the runes socketed in the item.
    'runeword': (None, 16),

    # Only exists when the item is personalized
    # The name of the character that personalized the item as a null-terminated string of 7-bit-wide characters.
    'personalized_value': (None, None),

    # Only exists if the item is a tome (of identify or town portal)
    'tome': (None, 5),

    # Unknown (denoted as 'timestamp' in various places)
    'unknown_11': (None, 1),

    # Only exists if the item is an armor
    # Defense of the armor.
    'defense_value': (None, 16),

    # Only exists if the item is an armor or a weapon (i.e. the item code is found in Armor.txt or Weapons.txt)
    'max_durability': (None, 9),

    # Only exists if the item's max durability is greater than zero
    # The first 8 bits are the item's current durability. The last bit is unknown.
    'current_durability': (None, 9),

    # Only exists if the item is stackable
    # (i.e. the item code is found in Weapons.txt or Miscs.txt and the "stackable" column is 1)
    'quantity': (None, 9),

    # Only exists if the item is socketed
    # Total number of sockets in the item (both filled and/or unfilled)
    'total_sockets': (None, 4),

    # Only exists if the item's rarity is set
    # Set mods bit field, used later for reading the set property lists of the item
    'set_mod_bit_field': (None, 5),

    # List of magical mods of the item.
    'magic_mods': (None, None),

    # Only exists if the set mod bit field of the item is not zero
    'set_mods': (None, None),

    # Only exists if the item has a runeword given to it
    # A mod list containing the mods of the item that come from the runeword.
    'runeword_mods': (None, None)
}

LOCATIONS = {
    0: 'stored',
    1: 'equipped',
    2: 'belt',
    3: 'ground',
    4: 'cursor',
    6: 'socketed',
}

PANELS = {
    1: 'inventory',
    4: 'horadric_cube',
    5: 'stash'
}

EQUIPPED_LOCATIONS = {
    1: 'head',
    2: 'neck',
    3: 'torso',
    4: 'right_hand',
    5: 'left_hand',
    6: 'right_ring',
    7: 'left_ring',
    8: 'belt',
}

RARITIES = {
    0: 'invalid',
    1: 'low',
    2: 'normal',
    3: 'superior',
    4: 'magic',
    5: 'set',
    6: 'rare',
    7: 'unique',
    8: 'crafted',
    9: 'tempered'
}

ITEM_FOOTER = list('111111111')

START_DEFENSE_VALUE = -500
START_MAX_DURABILITY_VALUE = -90
START_CURRENT_DURABILITY_VALUE = -150

CATEGORIES = {
    'sorceress_armors': {
        'has_defense': True,
        'has_durability': True,
        'codes': [
            '6@I '
        ]
    },
    'armors': {
        'has_defense': True,
        'has_durability': True,
        'codes': [
            '843 ',
            '601 ',
            '@13 ',
            '@10 ',
        ]
    },
    'boots': {
        'has_defense': True,
        'has_durability': True,
        'codes': [
            '@40 ',
            '@41 '
        ]
    },
    'circlets': {
        'has_defense': True,
        'has_durability': True,
        'codes': [
            '@68 ',
            '@67 '
        ]
    },
    'helms': {
        'has_defense': True,
        'has_durability': True,
        'codes': [
            '615 ',
            '@45 ',
            '@46 '
        ]
    },
    'barbarian_helms': {
        'has_defense': True,
        'has_durability': True,
        'codes': [
            '@54 '
        ]
    },
    'shields': {
        'has_defense': True,
        'has_durability': True,
        'codes': [
            '621 '
        ]
    },
    'gloves': {
        'has_defense': True,
        'has_durability': True,
        'codes': [
            '@33 ',
            '@37 '
        ]
    },
    'belts': {
        'has_defense': True,
        'has_durability': True,
        'codes': [
            '@30 ',
            '@29 ',
            '627 '
        ]
    },
    'throwing_knives': {
        'has_durability': True,
        'codes': []
    },
    'axes': {
        'has_durability': True,
        'codes': [
            '120 ',
            '!34 ',
            '!55 '
        ]
    },
    'spears': {
        'has_durability': True,
        'codes': [
            '137 '
        ]
    },
    'swords': {
        'has_durability': True,
        'codes': [
            '08@ ',
        ]
    },
    'assassin_claws': {
        'has_durability': True,
        'codes': [
            'o18 ',
            '93@ '
        ]
    },
    'assassin_shields': {
        'has_defense': True,
        'has_durability': True,
        'codes': [
            '5@O ',
            '6@O ',
            '3@P '
        ]
    },
    'crossbows': {
        'codes': [
            'l55 ',
            'l53 '
        ]
    },
    'daggers': {
        'has_durability': True,
        'codes': [
            '144 '
        ]
    }
}
