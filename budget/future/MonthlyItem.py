import logging
from typing import List

logger = logging.getLogger("MonthBudgetItem")
logger.setLevel(logging.DEBUG)


class MonthBudgetItem():
    def __init__(self, miesiac, min, avg, max):
        self.miesiac = miesiac
        self.min = min
        self.avg = avg
        self.max = max

    def __str__(self) -> str:
        return "Miesiac={}; Min={}; Avg={}; Max={}".format(self.miesiac, self.min, self.avg, self.max)

    def __repr__(self) -> str:
        return self.__str__()


class MonthlyItem:
    def __init__(self, kategoria, subkategoria, detale, day_of_the_month, year, monthly_budget:List[MonthBudgetItem]):
        self.kategoria = kategoria
        self.subkategoria = subkategoria
        self.detale = detale
        self.day_of_the_month = day_of_the_month
        self.year = year
        self.monthly_budget = monthly_budget

    def __str__(self) -> str:
        return "Kategoria={}; Subkategoria={}; Detale={}; Dzien miesiaca={}; Rok={}; Budzet={}".format(
            self.kategoria, self.subkategoria, self.detale, self.day_of_the_month, self.year, self.monthly_budget)

    def __repr__(self) -> str:
        return self.__str__()
