import openpyxl as xl


class ColumnLetterLogic:


    @staticmethod
    def add(column_letter, addition):
        """加算。
        """
        return xl.utils.get_column_letter(xl.utils.column_index_from_string(column_letter) + addition)
