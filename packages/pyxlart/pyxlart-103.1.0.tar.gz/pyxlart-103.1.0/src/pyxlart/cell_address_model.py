import openpyxl as xl
import re


class CellAddressModel():
    """セル・アドレス・モデル。
    """


    _code_pattern = re.compile(r'([A-Z]+)(\d+)')


    @classmethod
    def from_code(clazz, code):
        result = clazz._code_pattern.match(code)

        if not result:
            raise ValueError(f"コード読取失敗。 {code=}")

        column_th   = xl.utils.column_index_from_string(result.group(1))
        row_th      = int(result.group(2))

        return CellAddressModel(
                column_th   = column_th,
                row_th      = row_th)


    def __init__(self, column_th, row_th):
        self._column_th = column_th
        self._row_th = row_th


    @property
    def column_th(self):
        return self._column_th


    @property
    def row_th(self):
        return self._row_th


    def to_code(self):
        return f"{xl.utils.get_column_letter(self._column_th)}{self._row_th}"


    def dump_string(self):
        return f"""{{"column_th"={self._column_th}, "row_th"={self._row_th}}}"""
