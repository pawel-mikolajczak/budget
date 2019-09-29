import logging
from datetime import datetime

logger = logging.getLogger("TimeItem")
logger.setLevel(logging.DEBUG)


class TimeItem:
    def __init__(self, data, kategoria, subkategoria, detale, minimum, avg, maximum):
        self.data = data
        self.maximum = maximum
        self.avg = avg
        self.minimum = minimum
        self.detale = detale
        self.subkategoria = subkategoria
        self.kategoria = kategoria

        logger.debug(
            "IrregularItem init {}, {}, {}, {}, {}, {}, {}".format(data, kategoria, subkategoria, detale, minimum, avg,
                                                                   maximum))

    def __str__(self) -> str:
        return "Data={}; Kategoria={}; Subkategoria={}; Detale={}; Minimum={}; AVG={}; Maximum={}".format(
            self.get_date(self.data), self.kategoria, self.subkategoria, self.detale, self.minimum, self.avg,
            self.maximum)

    def __repr__(self) -> str:
        return self.__str__()

    def get_date(d) -> datetime:
        return datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
