import logging

import pandas as pd

from budget.accounts.AccountItem import AccountItem

logger = logging.getLogger("AccountsService")

# =============================================
# constants
# =============================================
col_data = "Data"

# =============================================
# konta
# =============================================
konta = ["K - Inteligo Paweł", "K - Inteligo Agatka", "K - Gotówka PLN", "K - Auto", "K - Poduszka bezpieczeństwa",
         "K - Wakacje", "K - Filip", "K - Tomek", "K - Santander"]


# =============================================
# Accounts Service
# =============================================

class AccountsService:
    def process_items(self, input_file_path):
        xslx = pd.ExcelFile(input_file_path)

        items = list()

        for konto in konta:
            logger.info("Processing account: '{}' started...".format(konto))
            records_processed = self.process_account(xslx, konto, items)
            items.extend(records_processed)
            logger.info(
                "Processing account: '{}' finished. Number of records: {}".format(konto, records_processed.__len__()))

        return items

    @staticmethod
    def process_account(xslx, konto, items):
        df = pd.read_excel(xslx, '%s' % konto)

        accounts = list()

        for index, row in df.iterrows():
            a = AccountItem(konto, row[col_data], row["Opis"], row["Kwota"], row["Bilans"])
            accounts.append(a)

        return accounts

    def store_konta(self, konta:list, database):
        logger.info("Storing accounts to database: {}...".format(konta.__len__()))
        for konto in konta:
            database.add_konto(konto.typ, konto.data, konto.opis, konto.kwota, konto.bilans)
        logger.info("Storing accounts to database finished: {}...".format(konta.__len__()))

    def process_sum_konta(self, database):
        return database.select_data("SELECT "
                                    "   DATE(data, 'Start of month') [miesiac], "
                                    "   konto, "
                                    "   SUM(kwota) [suma] "
                                    "FROM konta "
                                    "GROUP BY DATE(data, 'Start of month'), konto "
                                    "ORDER BY 1 DESC, 2 ASC")

    def process_konta(self, database):
        return database.select_data("SELECT DISTINCT konto "
                                    "FROM konta ORDER BY 1 ASC")
