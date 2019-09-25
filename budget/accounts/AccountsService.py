import pandas as pd

# =============================================
# constants
# =============================================
from budget.accounts.AccountItem import AccountItem

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

        items = []

        for konto in konta:
            self.process_account(xslx, konto, items)

        return items

    @staticmethod
    def process_account(xslx, konto, items):
        df = pd.read_excel(xslx, '%s' % konto)

        for index, row in df.iterrows():
            a = AccountItem(konto, row[col_data], row["Opis"], row["Kwota"], row["Bilans"])
            items.append(a)

    def store_konta(self, konta, database):
        for konto in konta:
            database.add_konto(konto.typ, konto.data, konto.opis, konto.kwota, konto.bilans)