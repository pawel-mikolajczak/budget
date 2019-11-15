import logging

from budget.future.MonthlyItem import MonthBudgetItem

logger = logging.getLogger("AccountCashflowItem")
logger.setLevel(logging.DEBUG)


class AccountCashflowItem(MonthBudgetItem):
    def __init__(self, konto, miesiac, min, avg, max):
        super().__init__(miesiac, min, avg, max)
        self.konto = konto

    def __str__(self) -> str:
        return "Konto={}; Miesiac={}; Min={}; Avg={}; Max={}".format(self.konto, self.miesiac, self.min, self.avg,
                                                                     self.max)

    def __repr__(self) -> str:
        return self.__str__()
