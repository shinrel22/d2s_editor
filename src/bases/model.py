from src.common.utils import make_byte_array_from_hex


class Model(object):
    def __init__(self, data: str):
        self._raw_data = data
        self._data = make_byte_array_from_hex(data)

    def find_index(self,
                   query: list,
                   offset: int = None,
                   limit: int = None):

        if not offset:
            offset = 0

        if not limit:
            limit = len(self._data)

        result = None
        length = len(query)
        data_to_search = self._data[offset:limit]
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
