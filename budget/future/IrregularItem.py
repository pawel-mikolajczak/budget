import logging
from datetime import datetime

logger = logging.getLogger("IrregularItem")
logger.setLevel(logging.INFO)


class IrregularItem:
    def __init__(self, data, kategoria, podkategoria, detale, minimum, avg, maximum, finally_paid, final_paid_date,
                 comment):
        self.data = data
        self.comment = comment
        self.final_paid_date = final_paid_date
        self.finally_paid = finally_paid
        self.maximum = maximum
        self.avg = avg
        self.minimum = minimum
        self.detale = detale
        self.podkategoria = podkategoria
        self.kategoria = kategoria

        logger.debug(
            "IrregularItem init {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(data, kategoria, podkategoria, detale,
                                                                               minimum, avg, maximum, finally_paid,
                                                                               final_paid_date, comment))

    def __str__(self) -> str:
        return "Data={}; Kategoria={}; Podkategoria={}; Detale={}; Minimum={}; AVG={}; Maximum={}".format(
            self.get_date(self.data), self.kategoria, self.podkategoria, self.detale, self.minimum, self.avg,
            self.maximum)

    def __repr__(self) -> str:
        return self.__str__()

    def get_date(d) -> datetime:
        return datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
