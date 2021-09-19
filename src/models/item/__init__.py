from src.bases.errors import Error
from src.bases.model import Model
from src.common.constants.item import (
    EAR_STRUCTURE, NON_EAR_STRUCTURE, RARITIES,
    BASE_STRUCTURE, LOCATIONS, PANELS, EQUIPPED_LOCATIONS, ITEM_FOOTER,
    CATEGORIES, START_DEFENSE_VALUE, START_MAX_DURABILITY_VALUE,
    START_CURRENT_DURABILITY_VALUE
)
from src.common.constants.modifies import MODIFIES, MODIFY_ID_LENGTH
from src.common.utils import (
    bin_to_hex, bin_to_dec, split_array, dec_to_bin, make_byte_array_from_hex
)


class Item(Model):
    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.bin_data = self._parse_data_to_bit()

    def _read_data(self, index, length):
        value = self.bin_data[index: index + length]
        return bin_to_dec(''.join(reversed(value)))

    def _parse_data_to_bit(self):

        # little endian
        reversed_data = reversed(self._data)

        joined_data = ''.join(reversed_data)

        bin_data = dec_to_bin(int(joined_data, 16))

        return list(reversed(bin_data))

    @property
    def is_socketed(self):
        index, length = BASE_STRUCTURE['is_socketed']
        value = self.bin_data[index]
        return value == '1'

    @property
    def is_ear(self):
        index, length = BASE_STRUCTURE['is_ear']
        value = self.bin_data[index]
        return value == '1'

    @property
    def is_simple(self):
        index, length = BASE_STRUCTURE['is_simple']
        value = self.bin_data[index]
        return value == '1'

    @property
    def location(self):
        index, length = BASE_STRUCTURE['location']
        value = self.bin_data[index:index + length][::-1]
        value = ''.join(value)
        value = bin_to_dec(value)
        return LOCATIONS.get(value)

    @property
    def equipped_location(self):
        index, length = BASE_STRUCTURE['equipped_location']
        value = self.bin_data[index:index + length][::-1]
        value = ''.join(value)
        value = bin_to_dec(value)
        return EQUIPPED_LOCATIONS.get(value)

    @property
    def panel(self):
        index, length = BASE_STRUCTURE['panel']
        value = self.bin_data[index: index + length][::-1]
        value = ''.join(value)
        value = bin_to_dec(value)
        return PANELS.get(value)

    @property
    def x_coordinate(self):
        index, length = BASE_STRUCTURE['x_coordinate']
        value = self.bin_data[index: index + length][::-1]
        value = ''.join(value)
        return bin_to_dec(value)

    @property
    def y_coordinate(self):
        index, length = BASE_STRUCTURE['y_coordinate']
        value = self.bin_data[index: index + length][::-1]
        value = ''.join(value)
        return bin_to_dec(value)

    @property
    def type_code(self):
        if self.is_ear:
            return None
        index, length = NON_EAR_STRUCTURE['type_code']
        value = self.bin_data[index:index + length]
        result = ''
        for v in split_array(value, 8, padding='0'):
            joined_v = ''.join(reversed(v))
            dec_v = bin_to_dec(joined_v)
            letter = chr(dec_v)
            result += letter
        return result

    @property
    def id(self):
        if self.is_ear or self.is_simple:
            return None
        index, length = NON_EAR_STRUCTURE['unique_id']
        value = self.bin_data[index:index + length][::-1]
        return bin_to_dec(''.join(value))

    @property
    def level(self):
        if self.is_ear or self.is_simple:
            return None
        return self._read_data(*NON_EAR_STRUCTURE['level'])

    @property
    def rarity(self):
        if self.is_ear or self.is_simple:
            return None

        return RARITIES.get(self._read_data(*NON_EAR_STRUCTURE['rarity']))

    @property
    def has_custom_graphic(self):
        if self.is_ear or self.is_simple:
            return None
        return self._read_data(*NON_EAR_STRUCTURE['has_custom_graphic']) > 0

    @property
    def has_class_spec_index(self):
        if self.is_ear or self.is_simple:
            return None

        has_custom_graphic_index, has_custom_graphic_length = \
            NON_EAR_STRUCTURE['has_custom_graphic']
        _, custom_graphic_length = NON_EAR_STRUCTURE['custom_graphic']

        result = has_custom_graphic_index + has_custom_graphic_length

        if self.has_custom_graphic:
            result += custom_graphic_length

        return result

    @property
    def has_class_spec(self):
        if self.has_class_spec_index is None:
            return None

        _, length = NON_EAR_STRUCTURE['has_class_spec']
        return self._read_data(self.has_class_spec_index, length) > 0

    @property
    def rarity_details(self):
        if self.is_ear or self.is_simple:
            return None

        result = {
            'rarity': self.rarity
        }
        _, has_class_spec_length = NON_EAR_STRUCTURE['has_class_spec']
        details_index = self.has_class_spec_index + has_class_spec_length

        if self.has_class_spec:
            _, class_spec_length = NON_EAR_STRUCTURE['class_spec']
            details_index += class_spec_length

        result['index'] = details_index

        if self.rarity in ['rare', 'crafted']:
            _, prefix_id_length = NON_EAR_STRUCTURE[
                'cr_pf_type_id']
            _, suffix_id_length = NON_EAR_STRUCTURE[
                'cr_sf_type_id']

            prefix_id_index = details_index
            bin_prefix_id = reversed(
                self.bin_data[
                prefix_id_index: prefix_id_index + prefix_id_length]
            )
            prefix_id = bin_to_dec(''.join(bin_prefix_id))
            result['prefix_id_index'] = prefix_id_index
            result['prefix_id'] = prefix_id

            suffix_id_index = prefix_id_index + prefix_id_length
            bin_suffix_id = reversed(self.bin_data[
                                     suffix_id_index: suffix_id_index + suffix_id_length])
            suffix_id = bin_to_dec(''.join(bin_suffix_id))
            result['suffix_id_index'] = suffix_id_index
            result['suffix_id'] = suffix_id

            affixes_index = suffix_id_index + suffix_id_length
            result['affixes_index'] = affixes_index

            affixes = []

            # there are total of 6 affixes
            current_aff_index = affixes_index
            aff_id_length = 11
            for i in range(6):
                aff_exist = self.bin_data[
                            current_aff_index: current_aff_index + 1] == ['1']
                if aff_exist:
                    aff_id_index = current_aff_index + 1
                    bin_aff_id = reversed(
                        self.bin_data[
                        aff_id_index: aff_id_index + aff_id_length]
                    )
                    aff_id = bin_to_dec(''.join(bin_aff_id))
                    affixes.append({
                        'id': aff_id,
                        'id_index': aff_id_index
                    })
                    current_aff_index += (aff_id_length + 1)
                else:
                    current_aff_index += 1
            result['affixes'] = affixes

            result['length'] = current_aff_index - details_index

        elif self.rarity == 'magic':
            _, pf_type_id_length = NON_EAR_STRUCTURE['magic_pf_type_id']
            _, sf_type_id_length = NON_EAR_STRUCTURE['magic_sf_type_id']

            prefix_id_index = details_index
            result['prefix_id_index'] = prefix_id_index
            bin_prefix_id = reversed(self.bin_data[
                                     prefix_id_index: prefix_id_index + pf_type_id_length])
            prefix_id = bin_to_dec(''.join(bin_prefix_id))
            result['prefix_id'] = prefix_id

            suffix_id_index = prefix_id_index + pf_type_id_length
            bin_suffix_id = reversed(self.bin_data[
                                     suffix_id_index: suffix_id_index + sf_type_id_length])
            suffix_id = bin_to_dec(''.join(bin_suffix_id))
            result['suffix_id_index'] = suffix_id_index
            result['suffix_id'] = suffix_id

            result['length'] = suffix_id_index + sf_type_id_length - details_index

        elif self.rarity == 'unique':
            _, quality_id_length = NON_EAR_STRUCTURE['unique_quality_id']
            bin_quality_id = reversed(
                self.bin_data[details_index: details_index + quality_id_length]
            )
            quality_id = bin_to_dec(''.join(bin_quality_id))
            result['quality_id'] = quality_id

            result['length'] = quality_id_length

        elif self.rarity == 'set':
            _, quality_id_length = NON_EAR_STRUCTURE['set_quality_id']
            bin_quality_id = reversed(
                self.bin_data[details_index: details_index + quality_id_length]
            )
            quality_id = bin_to_dec(''.join(bin_quality_id))
            result['quality_id'] = quality_id

            result['length'] = quality_id_length

        elif self.rarity == 'superior':
            _, quality_id_length = NON_EAR_STRUCTURE['superior_quality_id']
            bin_quality_id = self.bin_data[details_index: details_index + quality_id_length]
            quality_id = bin_to_dec(''.join(reversed(bin_quality_id)))
            result['quality_id'] = quality_id
            result['length'] = quality_id_length

        return result

    @property
    def set_mod_bit_field_index(self):
        total_socket_index = self.total_socket_index

        if self.is_socketed:
            _, total_socket_length = NON_EAR_STRUCTURE['total_sockets']
            return total_socket_index + total_socket_length

        return total_socket_index

    @property
    def magic_mods_index(self):
        set_mod_bit_field_index = self.set_mod_bit_field_index

        if self.rarity == 'set':
            _, set_mod_bit_field_length = NON_EAR_STRUCTURE['set_mod_bit_field']
            return set_mod_bit_field_index + set_mod_bit_field_length

        return set_mod_bit_field_index

    @property
    def category(self):
        if self.is_ear:
            return None
        result = None
        for k, v in CATEGORIES.items():
            if self.type_code in v['codes']:
                result = k
        return result

    @property
    def has_defense(self):
        if self.is_ear or self.is_simple:
            return False

        category = CATEGORIES.get(self.category)
        if not category:
            return False

        return category.get('has_defense')

    @property
    def has_durability(self):
        if self.is_ear or self.is_simple:
            return False

        category = CATEGORIES.get(self.category)
        if not category:
            return False

        return category.get('has_durability')

    @property
    def is_stackable(self):
        if self.is_ear or self.is_simple:
            return False

        category = CATEGORIES.get(self.category)
        if not category:
            return False

        return category.get('is_stackable')

    @property
    def defense_index(self):
        rarity_details = self.rarity_details

        result = rarity_details['index'] + rarity_details['length']

        # unknown_11 bit
        result += 1

        return result

    @property
    def max_durability_index(self):
        defense_index = self.defense_index
        if self.has_defense:
            _, defense_length = NON_EAR_STRUCTURE['defense_value']
            return defense_index + defense_length
        return defense_index

    @property
    def defense_value(self):
        if not self.has_defense:
            return None
        index = self.defense_index
        _, length = NON_EAR_STRUCTURE['defense_value']
        result_as_bin = reversed(self.bin_data[index: index + length])
        return bin_to_dec(''.join(result_as_bin)) + START_DEFENSE_VALUE

    @property
    def max_durability(self):
        if not self.has_durability:
            return None

        index = self.max_durability_index
        _, length = NON_EAR_STRUCTURE['max_durability']
        result_as_bin = reversed(self.bin_data[index: index + length])

        return bin_to_dec(''.join(result_as_bin)) + START_MAX_DURABILITY_VALUE

    @property
    def current_durability_index(self):
        max_durability_index = self.max_durability_index
        if self.has_durability:
            _, max_durability_length = NON_EAR_STRUCTURE['max_durability']
            return max_durability_index + max_durability_length

        return max_durability_index

    @property
    def current_durability(self):
        if not self.has_durability:
            return None
        index = self.current_durability_index
        _, length = NON_EAR_STRUCTURE['current_durability']
        result_as_bin = reversed(self.bin_data[index: index + length])
        return bin_to_dec(
            ''.join(result_as_bin)
        ) + START_CURRENT_DURABILITY_VALUE

    @property
    def quantity_index(self):
        current_durability_index = self.current_durability_index
        if self.has_durability:
            _, current_durability_length = NON_EAR_STRUCTURE['current_durability']
            return current_durability_index + current_durability_length
        return current_durability_index

    @property
    def total_socket_index(self):
        quantity_index = self.quantity_index
        if self.is_stackable:
            _, quantity_length = NON_EAR_STRUCTURE['quantity']
            return quantity_index + quantity_length
        return quantity_index

    @property
    def data(self):
        hex_data = bin_to_hex(
            ''.join(reversed(self.bin_data))
        )
        result = reversed(
            make_byte_array_from_hex(hex_data)
        )

        return result

    def save(self, file_path):
        with open(file_path, 'wb') as file_ref:
            file_ref.write(
                bytes.fromhex(''.join(self.data))
            )

    def update_id(self, value: int):
        if self.is_ear or self.is_simple:
            return
        id_index, id_length = NON_EAR_STRUCTURE['unique_id']
        value_as_bin = dec_to_bin(value, length=id_length)
        self.bin_data[id_index: id_index + id_length] = list(
            value_as_bin[::-1])

    def clear_magic_mods(self):
        if self.is_ear or self.is_simple:
            raise Error('UnsupportedAction')

        index = self.magic_mods_index
        length = len(self.bin_data) - index - len(ITEM_FOOTER)

        self.delete_data(index, length)

    def change_max_durability(self, value: int):
        if not self.has_durability:
            raise Error('UnsupportedAction',
                        'Item does not have durability')

        index = self.max_durability_index
        _, length = NON_EAR_STRUCTURE['max_durability']

        bin_value = dec_to_bin(value - START_MAX_DURABILITY_VALUE, length=length)

        self.edit(index, list(reversed(bin_value)))

    def update_location(self,
                        location: int,
                        panel: int,
                        x: int,
                        y: int,
                        equipped_location: int = None):

        # update location
        location_index, location_length = BASE_STRUCTURE['location']
        location_as_bin = dec_to_bin(location, length=location_length)[::-1]
        self.bin_data[location_index: location_index + location_length] = list(
            location_as_bin)

        # update panel
        panel_index, panel_length = BASE_STRUCTURE['panel']
        panel_as_bin = dec_to_bin(panel, length=panel_length)[::-1]
        self.bin_data[panel_index: panel_index + panel_length] = list(
            panel_as_bin)

        # update xy
        x_index, x_length = BASE_STRUCTURE['x_coordinate']
        y_index, y_length = BASE_STRUCTURE['y_coordinate']
        x_as_bin = dec_to_bin(x, length=x_length)[::-1]
        y_as_bin = dec_to_bin(y, length=y_length)[::-1]
        self.bin_data[x_index: x_index + x_length] = list(x_as_bin)
        self.bin_data[y_index: y_index + y_length] = list(y_as_bin)

    def edit(self, index: int, data: list):
        length = len(data)
        before = ''.join(self.bin_data[index - length:])
        self.bin_data[index: index + length] = data
        after = (' ' * length) + ''.join(self.bin_data[index:index + length])

        print('===== changes =====')
        print(before)
        print(after)

    def insert(self, index, data: list):
        length = len(data)
        before = '{}{}{}'.format(
            ''.join(self.bin_data[index - length:index]),
            (' ' * length),
            ''.join(self.bin_data[index: index + length])
        )
        for bit in reversed(data):
            self.bin_data.insert(index, bit)

        after = '{}{}'.format(
            ' ' * length,
            ''.join(data),
        )

        print('===== changes =====')
        print(before)
        print(after)

    def delete_data(self, index: int, length: int):
        before = ''.join(self.bin_data[index - length: index + length])
        after = '{}{}{}'.format(
            ''.join(self.bin_data[index - length:index]),
            ' ' * length,
            ''.join(self.bin_data[index + length:])
        )
        del self.bin_data[index: index + length]
        print('===== changes =====')
        print(before)
        print(after)

    def change_level(self, value: int):
        if self.is_ear or self.is_simple:
            return

        level_index, level_length = NON_EAR_STRUCTURE['level']
        bin_value = dec_to_bin(value, length=level_length)
        self.edit(level_index, list(reversed(bin_value)))

    def add_magic_mod(self, mod_id: int, values: dict = None):
        if self.is_ear or self.is_simple:
            raise Error(code='UnsupportedAction',
                        message='Cannot add mod of simple or ear item.')

        mod_data = self._gen_magic_mode_data(
            mod_id=mod_id,
            values=values
        )
        self.insert(self.magic_mods_index, mod_data)

    def edit_magic_mod(self, mod_id: int, from_values: dict, to_values: dict):
        if self.is_ear or self.is_simple:
            raise Error(code='UnsupportedAction',
                        message='Cannot edit mod of simple or ear item.')

        current_mod_data = self._gen_magic_mode_data(
            mod_id=mod_id,
            values=from_values
        )
        mod_index = self.find_data(
            query=current_mod_data,
            offset=self.magic_mods_index,
            limit=len(self.bin_data) - len(ITEM_FOOTER)
        )
        if mod_index is None:
            raise Error('ModNotFound', meta=from_values)

        new_mod_data = self._gen_magic_mode_data(mod_id=mod_id,
                                                 values=to_values)
        self.edit(mod_index, new_mod_data)

    def delete_magic_mode(self, mod_id: int, values: dict):
        if self.is_ear or self.is_simple:
            raise Error(code='UnsupportedAction',
                        message='Cannot delete mod from simple or ear item.')

        mod_data = self._gen_magic_mode_data(
            mod_id=mod_id,
            values=values
        )
        print(''.join(mod_data))
        mod_index = self.find_data(
            query=mod_data,
            offset=self.magic_mods_index,
            limit=len(self.bin_data) - len(ITEM_FOOTER)
        )
        if mod_index is None:
            raise Error('ModNotFound', message=str(mod_id))

        self.delete_data(mod_index, length=len(mod_data))

    def change_rarity(self, rarity_id: int, **kwargs):
        if self.is_ear or self.is_simple:
            raise Error('UnsupportedAction',
                        'Cannot change rarity of simple or ear item')

        rarity = RARITIES[rarity_id]

        current_rarity_details = self.rarity_details

        detail_index = current_rarity_details['index']

        new_detail_data = []

        if rarity == 'unique':
            _, quality_id_length = NON_EAR_STRUCTURE['unique_quality_id']
            quality_id = kwargs.get('quality_id') or 0
            bin_quality_id = dec_to_bin(value=quality_id,
                                        length=quality_id_length)
            new_detail_data.extend(reversed(bin_quality_id))

        elif rarity == 'magic':
            _, prefix_id_length = NON_EAR_STRUCTURE['magic_prefix_id']
            _, suffix_id_length = NON_EAR_STRUCTURE['magic_suffix_id']

            prefix_id = kwargs.get('suffix_id') or 0
            suffix_id = kwargs.get('suffix_id') or 0
            bin_prefix_id = dec_to_bin(
                value=prefix_id,
                length=prefix_id_length
            )
            bin_suffix_id = dec_to_bin(
                value=suffix_id,
                length=suffix_id_length
            )
            new_detail_data.extend(reversed(bin_prefix_id))
            new_detail_data.extend(reversed(bin_suffix_id))

        else:
            raise Error('UnsupportedRarity',
                        'Cannot change to this rarity')

        # delete current rarity details
        self.delete_data(
            index=current_rarity_details['index'],
            length=current_rarity_details['length']
        )

        # insert new detail data
        self.insert(detail_index, new_detail_data)

        # update rarity
        rarity_index, rarity_length = NON_EAR_STRUCTURE['rarity']
        bin_rarity = dec_to_bin(value=rarity_id, length=rarity_length)
        self.edit(rarity_index, list(reversed(bin_rarity)))

    def change_type_code(self, value: str):
        if self.is_ear:
            raise Error('UnsupportedAction',
                        'Cannot change type_code of ear items')

        new_data = []

        index, length = NON_EAR_STRUCTURE['type_code']

        for char in value:
            char_as_bin = dec_to_bin(
                value=ord(char),
                length=8
            )
            new_data.extend(reversed(char_as_bin))

        self.edit(index, new_data)

    @staticmethod
    def _gen_magic_mode_data(mod_id: int, values: dict = None):
        mod = MODIFIES[mod_id]
        if not values:
            values = {}

        mod_code = mod['code']

        result = list(reversed(dec_to_bin(mod_id, length=MODIFY_ID_LENGTH)))
        struct_data = []
        total_length = mod['length']

        if mod_code in ['+_min_dmg', '+_max_dmg']:
            value = values.get('value')

            value_st = list(filter(
                lambda x: x['code'] == 'value',
                mod['struct']
            ))[0]
            length = value_st['length']
            min_value = value_st.get('min_value', 0)
            max_value = bin_to_dec('1' * length)
            if value is None:
                value = max_value
            else:
                value = min(value - min_value, max_value)
            struct_data.extend(
                reversed(dec_to_bin(value, length=length))
            )
            if mod_code == '+_min_dmg':
                struct_data.extend(
                    list('111010000')
                )
                struct_data.extend(
                    reversed(dec_to_bin(value, length=11))
                )
                struct_data.extend(
                    list('111110010')
                )
                struct_data.extend(
                    reversed(dec_to_bin(value, length=10))
                )
            else:
                struct_data.extend(
                    list('000110000')
                )
                struct_data.extend(
                    reversed(dec_to_bin(value, length=11))
                )
                struct_data.extend(
                    list('000001010')
                )
                struct_data.extend(
                    reversed(dec_to_bin(value, length=10))
                )
        else:
            for st in mod['struct']:
                length = st['length']
                code = st['code']

                min_value = st.get('min_value', 0)
                max_value = bin_to_dec('1' * length)

                value = values.get(code)
                if value is None:
                    value = max_value
                else:
                    value = min(value - min_value, max_value)

                struct_data.extend(
                    reversed(dec_to_bin(value, length=length))
                )

        if len(struct_data) != total_length:
            raise Error('StructLengthMismatched')

        result.extend(struct_data)

        return result

    def print_data(self, offset: int = None, length: int = None):
        if not offset:
            offset = 0
        if length:
            data = self.bin_data[offset:offset + length]
        else:
            data = self.bin_data[offset:]

        print(''.join(data))

    def find_data(self, query: list,
                  offset: int = None,
                  limit: int = None):

        if not offset:
            offset = 0

        if not limit:
            limit = len(self.bin_data)

        result = None
        length = len(query)
        data_to_search = self.bin_data[offset:limit]
        for index, byte in enumerate(data_to_search):
            check_value = data_to_search[index: length + index]
            if len(check_value) < length:
                break

            if check_value == query:
                result = index
                break

        if result is None:
            return None

        return offset + result
