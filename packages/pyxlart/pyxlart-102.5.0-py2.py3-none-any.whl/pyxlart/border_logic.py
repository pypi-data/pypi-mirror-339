from openpyxl.styles.borders import Border


class BorderLogic:


    @staticmethod
    def add(base, addition):
        return Border(
                left    = BorderLogic._last(a=base.left    , b=addition.left),
                right   = BorderLogic._last(a=base.right   , b=addition.right),
                top     = BorderLogic._last(a=base.top     , b=addition.top),
                bottom  = BorderLogic._last(a=base.bottom  , b=addition.bottom))


    @staticmethod
    def _last(a, b):
        if b is not None:
            return b
        return a
