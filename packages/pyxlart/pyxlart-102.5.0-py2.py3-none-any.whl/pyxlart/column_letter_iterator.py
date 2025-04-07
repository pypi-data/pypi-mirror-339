import openpyxl as xl


class ColumnLetterIterator:


    def __init__(self, start, end):
        """初期化。

        Parameters
        ----------
        start : str
            開始列のアルファベット。
        end : str
            終了列のアルファベット。この終了列自身は含まない。
        """
        self._current_th = xl.utils.column_index_from_string(start)
        self._end_th = xl.utils.column_index_from_string(end)


    def __iter__(self):
        return self


    def __next__(self):
        if self._current_th < self._end_th:
            result = self._current_th
            self._current_th += 1
            return xl.utils.get_column_letter(result)
        else:
            raise StopIteration()
