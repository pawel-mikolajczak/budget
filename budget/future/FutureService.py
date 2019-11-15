import calendar
import datetime
import logging
from typing import List

import pandas as pd

from budget.db.DatabaseSupport import DatabaseSupport
from budget.future.AccountCashflowItem import AccountCashflowItem
from budget.future.IrregularItem import IrregularItem
from budget.future.MonthlyItem import MonthBudgetItem
from budget.future.MonthlyItem import MonthlyItem

DAYS_IN_A_FUTURE = 365 * 3

logger = logging.getLogger("FutureService")

# =============================================
# constants
# =============================================

transfery_kategorie = {
    "K - Inteligo Paweł": ["Na Inteligo Pawła", "Przelew z Inteligo Pawła"],
    "K - Inteligo Agatka": ["Na Inteligo Agatki", "Przelew z Inteligo Agatki"],
    "K - Gotówka PLN": ["Wypłata gotówki PLN", "Wpłata na konto PLN"],
    "K - Auto": ["Na auto", "Wyciągamy z auta"],
    "K - Poduszka bezpieczeństwa": ["Na poduszkę finansową", "Lądowanie na poduszce"],
    "K - Wakacje": ["Na wakacje", "Jedziemy na wakacje"],
    "K - Filip": ["Dla Filipka", "Przelew od Filipka"],
    "K - Tomek": ["Dla Tomka", "Przelew od Tomka"],
    "K - Santander": ["Na Santander", "Przelew z Santandera"]
}

# =============================================
# future_tabs
# =============================================
irregular_tab = "B - Nieregularne"
monthly_tab = "B - Miesięczne"
mbank_stan_konta_tab = "K - mBank"


# =============================================
# Future Service
# =============================================

class FutureService:
    def read_irregular_items(self, input_file_path):
        xslx = pd.ExcelFile(input_file_path)

        items = []

        df = pd.read_excel(xslx, '%s' % irregular_tab)

        for index, row in df.iterrows():
            i = IrregularItem(row["Data"], row["Kategoria"], row["Podkategoria"], row["Detale"], row["Minimum"],
                              row["AVG"], row["Maximum"], row["Finalnie zapłacono"], row["Finalna data zakupu"],
                              row["Komentarz"])
            items.append(i)

        return items

    def store_irregular_items(self, items: List[IrregularItem], database: DatabaseSupport):
        logger.info("Storing irregular items to database: {}...".format(items.__len__()))
        for item in items:
            query = "INSERT INTO nieregularne ('data', 'kategoria', 'subkategoria', 'detale', 'minimum', 'average', 'maximum', 'finally_paid', 'final_paid_date', 'comments') VALUES ('{}','{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                item.data, item.kategoria, item.subkategoria, item.detale, item.minimum, item.avg, item.maximum,
                item.finally_paid, item.final_paid_date, item.comment)
            database.insert_data(query, "Irregular item")
        logger.info("Storing irregular items to database finished: {}...".format(items.__len__()))

    def process_days(self, database: DatabaseSupport):
        start_date = database.select_data("SELECT MAX(data) [data] FROM mbank_stan_konta")[0][0]
        database.select_data_via_script("scripts/queries/process_dni.sql", [start_date])
        return database.select_data("SELECT dzien FROM dni ORDER BY 1 ASC")

    def process_cashflow(self, database: DatabaseSupport):
        database.select_data_via_script("scripts/queries/future_cashflow.sql")
        return database.select_data("SELECT data, kategoria, subkategoria, detale, min, avg, max FROM cashflow_details ORDER BY 1 ASC")

    def read_monthly_budget(self, input_file_path):
        xslx = pd.ExcelFile(input_file_path)

        items = []

        df = pd.read_excel(xslx, '%s' % monthly_tab)

        for index, row in df.iterrows():
            monthly_budget = list()
            monthly_budget.append(MonthBudgetItem(1, row["1Min"], row["1Avg"], row["1Max"]))
            monthly_budget.append(MonthBudgetItem(2, row["2Min"], row["2Avg"], row["2Max"]))
            monthly_budget.append(MonthBudgetItem(3, row["3Min"], row["3Avg"], row["3Max"]))
            monthly_budget.append(MonthBudgetItem(4, row["4Min"], row["4Avg"], row["4Max"]))
            monthly_budget.append(MonthBudgetItem(5, row["5Min"], row["5Avg"], row["5Max"]))
            monthly_budget.append(MonthBudgetItem(6, row["6Min"], row["6Avg"], row["6Max"]))
            monthly_budget.append(MonthBudgetItem(7, row["7Min"], row["7Avg"], row["7Max"]))
            monthly_budget.append(MonthBudgetItem(8, row["8Min"], row["8Avg"], row["8Max"]))
            monthly_budget.append(MonthBudgetItem(9, row["9Min"], row["9Avg"], row["9Max"]))
            monthly_budget.append(MonthBudgetItem(10, row["10Min"], row["10Avg"], row["10Max"]))
            monthly_budget.append(MonthBudgetItem(11, row["11Min"], row["11Avg"], row["11Max"]))
            monthly_budget.append(MonthBudgetItem(12, row["12Min"], row["12Avg"], row["12Max"]))

            i = MonthlyItem(row["Kategoria"], row["Podkategoria"], row["Detale"], row["Dnia miesiąca"],
                            row["Rok"], monthly_budget)
            items.append(i)

        return items

    def store_monthly_items(self, items: List[MonthlyItem], database: DatabaseSupport):
        logger.info("Storing monthly items to database: {}...".format(items.__len__()))
        for item in items:
            for mb in item.monthly_budget:
                day_of_month = None
                if (item.day_of_the_month == "LAST"):
                    day_of_month = calendar.monthrange(item.year, mb.miesiac)[1]
                else:
                    day_of_month = int(item.day_of_the_month)
                data = datetime.date(item.year, mb.miesiac, day_of_month)

                query = "INSERT INTO miesieczne ('data', 'kategoria', 'subkategoria', 'detale', 'minimum', 'average', 'maximum') VALUES ('{}','{}','{}', '{}', '{}', '{}', '{}')".format(
                    data, item.kategoria, item.subkategoria, item.detale, mb.min, mb.avg, mb.max)
                database.insert_data(query, "Monthly item")
        logger.info("Storing irregular items to database finished: {}...".format(items.__len__()))

    def process_mbank_stan_konta(self, input_file_path, database):
        xslx = pd.ExcelFile(input_file_path)

        items = []

        df = pd.read_excel(xslx, '%s' % mbank_stan_konta_tab)

        for index, row in df.iterrows():
            query = "INSERT INTO mbank_stan_konta ('data', 'stan_konta') VALUES ('{}','{}')".format(row["Data"],
                                                                                                    row["Stan konta"])
            database.insert_data(query, "mBank Stan Konta")

        return items

    def process_monthly_budget(self, database:DatabaseSupport):
        database.select_data_via_script("scripts/queries/monthly_budget.sql")

    def process_monthly_budget_execution(self, database):
        database.select_data_via_script("scripts/queries/monthly_budget_execution.sql")
        return database.select_data(
            "SELECT miesiac, kategoria, subkategoria, kwota FROM monthly_budget_execution ORDER BY 1 ASC, 2 ASC, 3 ASC")

    def process_future_accounts_cashflow(self, database:DatabaseSupport):
        items = []

        for konto in transfery_kategorie.keys():
            subkategorie = transfery_kategorie[konto]
            subkategorie_string = ["', '".join(subkategorie)]
            account_results_per_month = database.select_data_via_script("scripts/queries/konta_cashflow.sql", subkategorie_string)
            for result in account_results_per_month:
                item = AccountCashflowItem(konto, result[0], result[1], result[2], result[3])
                items.append(item)

        return items