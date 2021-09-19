import numpy as np
import time

from src.bases.model import Model
from src.common.constants.d2s_format import (
    ITEM_LIST_HEADER, ITEM_LIST_FOOTER, ITEM_HEADER, STRUCTURE,
    MERC_ITEM_LIST_HEADER, FOOTER
)
from src.models.item import Item
from src.common.utils import dec_to_hex, make_byte_array_from_hex


class Character(Model):
    def __init__(self, *args, **kwargs):
        super(Character, self).__init__(*args, **kwargs)
        self.items = self._parse_items(self.item_start_index, self.item_list_footer_index)

        self.merc_items = []
        if self.merc_name_id:
            self.merc_items = self._parse_items(self.merc_item_start_index)

    @property
    def version(self):
        index, length = STRUCTURE['version']
        value = self._data[index:index + length]
        value = ''.join(value[::-1])
        return int(value, 16)

    @property
    def item_list_header_index(self):
        return self.find_index(ITEM_LIST_HEADER)

    @property
    def item_list_footer_index(self):
        return self.find_index(ITEM_LIST_FOOTER)

    @property
    def item_start_index(self):
        return self.item_list_header_index + 4

    @property
    def merc_name_id(self):
        index, length = STRUCTURE['mercenary_name_id']
        value = self._data[index: index + length][::-1]
        value = ''.join(value)
        return int(value, 16)

    @property
    def merc_item_list_header_index(self):
        return self.find_index(MERC_ITEM_LIST_HEADER,
                               offset=self.item_list_footer_index + len(ITEM_LIST_FOOTER))

    @property
    def merc_item_start_index(self):
        return self.merc_item_list_header_index + 4

    @property
    def footer_index(self):
        return len(self._data) - len(FOOTER)

    def _parse_items(self, start: int, end: int = None):

        if not end:
            end = self.footer_index

        result = []
        items_data = self._data[start:end]
        items_data = ''.join(items_data)
        item_header_as_str = ''.join(ITEM_HEADER)
        items_data = items_data.split(item_header_as_str)

        for i in items_data:
            if not i:
                continue
            item_data = item_header_as_str + i
            result.append(Item(item_data))

        return result

    @staticmethod
    def calculate_checksum(data):
        index, length = STRUCTURE['checksum']
        result = np.int32(0)
        for i, b in enumerate(data):
            if index <= i < (index + length):
                b = '00'
            result = np.int32((result << 1) + np.int32(int(b, 16)) + (result < 0))
        if result < 0:
            result += (int('ffffffff', 16) + 1)
        return result

    def save(self, file_path: str, backup_path: str = None):
        result = self._data[:self.item_list_header_index]
        item_list_data = []
        item_list_data.extend(ITEM_LIST_HEADER)
        counted_items = list(filter(
            lambda x: x.location != 'socketed',
            self.items
        ))
        total_items_data = reversed(make_byte_array_from_hex(
            dec_to_hex(len(counted_items), length=4)
        ))
        item_list_data.extend(total_items_data)
        for item in self.items:
            item_list_data.extend(item.data)
        item_list_data.extend(ITEM_LIST_FOOTER)
        result.extend(item_list_data)

        if self.merc_name_id:
            merc_item_list_data = []
            merc_item_list_data.extend(MERC_ITEM_LIST_HEADER)
            merc_counted_items = list(filter(
                lambda x: x.location != 'socketed',
                self.merc_items
            ))
            merc_item_list_data.extend(reversed(make_byte_array_from_hex(
                dec_to_hex(len(merc_counted_items),
                           length=4)
            )))
            for merc_item in self.merc_items:
                merc_item_list_data.extend(merc_item.data)
            result.extend(merc_item_list_data)

        result.extend(FOOTER)

        file_size_index, file_size_length = STRUCTURE['file_size']
        file_size = make_byte_array_from_hex(dec_to_hex(len(result), length=file_size_length * 2))[::-1]
        result[file_size_index: file_size_index + file_size_length] = file_size

        checksum_index, checksum_length = STRUCTURE['checksum']
        checksum = self.calculate_checksum(result)
        checksum = make_byte_array_from_hex(dec_to_hex(
            checksum,
            length=checksum_length * 2
        ))[::-1]
        result[checksum_index: checksum_index + checksum_length] = checksum

        # backup
        if backup_path:
            with open(backup_path, 'wb') as file_ref:
                file_ref.write(bytes.fromhex(self._raw_data))

        # origin = make_byte_array_from_hex(self._raw_data)
        #
        # for index, byte in enumerate(result):
        #     if byte != origin[index]:
        #         print('diff', index, byte, origin[index])

        with open(file_path, 'wb') as file_ref:
            file_ref.write(bytes.fromhex(''.join(result)))

    def add_item_from_file(self,
                           file_path: str,
                           location: int,
                           panel: int,
                           x: int,
                           y: int):
        with open(file_path, 'rb') as file_ref:
            item_data = file_ref.read().hex()
        item = Item(item_data)
        item.update_location(
            location=location,
            panel=panel,
            x=x,
            y=y
        )
        item.update_id(int(time.time()))
        self.items.append(item)
