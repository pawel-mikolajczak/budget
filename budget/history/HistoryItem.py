import logging
import math
from datetime import datetime

logger = logging.getLogger("HistoryItem")
logger.setLevel(logging.INFO)


class HistoryItem:
    def __init__(self, typ, miesiac, kategoria, subkategoria, kwota):
        self.typ = typ
        self.miesiac = miesiac
        self.kategoria = kategoria
        self.subkategoria = subkategoria
        if math.isnan(kwota):
            self.kwota = float("0.0")
        else:
            self.kwota = kwota
        logger.debug("{} init {}, {}, {}, {}".format(typ, miesiac, kategoria, subkategoria, kwota))

    def __str__(self) -> str:
        return "Typ={}; Miesiąc={}; Kategoria={}; Subkategoria={}; Kwota={}".format(self.typ,
                                                                                    self.get_miesiac_as_date(),
                                                                                    self.kategoria,
                                                                                    self.subkategoria,
                                                                                    self.kwota)

    def __repr__(self) -> str:
        return self.__str__()

    def get_miesiac_as_date(self) -> datetime:
        return datetime.strptime(str(self.miesiac), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
