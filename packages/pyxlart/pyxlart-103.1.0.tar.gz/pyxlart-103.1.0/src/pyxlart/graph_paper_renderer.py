import openpyxl as xl


class GraphPaperRenderer():
    """方眼紙を描画します。
    """

    @staticmethod
    def render(left_th, top_th, width, height, ws):
        """描画。

        Parameters
        ----------
        left_th : int
            開始列。1から始まる数。
        top_th : int
            開始行。1から始まる数。
        width : int
            横のセル数。
        height : int
            縦のセル数。
        ws : Worksheet
            ワークシート。
        """

        # 行の横幅
        for column_th in range(left_th, width+1):
            column_letter = xl.utils.get_column_letter(column_th)
            ws.column_dimensions[column_letter].width = 2.7    # 2.7 characters = about 30 pixels

        # 列の高さ
        for row_th in range(top_th, height+1):
            ws.row_dimensions[row_th].height = 15    # 15 points = about 30 pixels
