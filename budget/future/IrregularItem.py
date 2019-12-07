import logging
from datetime import datetime

logger = logging.getLogger("IrregularItem")
logger.setLevel(logging.DEBUG)


class IrregularItem:
    def __init__(self, konto, data, kategoria, subkategoria, detale, minimum, avg, maximum, finally_paid, final_paid_date,
                 comment):
        self.konto = konto
        self.data = data
        self.comment = comment
        self.final_paid_date = final_paid_date
        self.finally_paid = finally_paid
        self.maximum = maximum
        self.avg = avg
        self.minimum = minimum
        self.detale = detale
        self.subkategoria = subkategoria
        self.kategoria = kategoria

        logger.debug(
            "IrregularItem init {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(konto, data, kategoria, subkategoria, detale,
                                                                               minimum, avg, maximum, finally_paid,
                                                                               final_paid_date, comment))

    def __str__(self) -> str:
        return "Konto={}; Data={}; Kategoria={}; Subkategoria={}; Detale={}; Minimum={}; AVG={}; Maximum={}".format(
            self.get_date(self.data), self.kategoria, self.subkategoria, self.detale, self.minimum, self.avg,
            self.maximum)

    def __repr__(self) -> str:
        return self.__str__()

    def get_date(d) -> datetime:
        return datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
