import logging
import math
from datetime import datetime

logger = logging.getLogger("AccountItem")
logger.setLevel(logging.INFO)

class AccountItem:
    def __init__(self, typ, data, opis, kwota, bilans):
        self.typ = typ
        self.data = data
        self.opis = opis

        if math.isnan(kwota):
            self.kwota = float("0.0")
        else:
            self.kwota = kwota

        if math.isnan(bilans):
            self.bilans = float("0.0")
        else:
            self.bilans = bilans

        logger.debug("Konto init {}, {}, {}, {}, {}".format(typ, data, opis, kwota, bilans))

    def __str__(self) -> str:
        return "Typ={}; Data={}; Opis={}; Kwota={}; Bilans={}".format(self.typ,
                                                                      self.get_date(),
                                                                      self.opis,
                                                                      self.kwota,
                                                                      self.bilans)

    def __repr__(self) -> str:
        return self.__str__()

    def get_date(self) -> datetime:
        return datetime.strptime(str(self.miesiac), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
