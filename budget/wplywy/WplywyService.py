import pandas as pd

from budget.wplywy.Wplyw import Wplyw

# =============================================
# constants
# =============================================

col_miesiac = "Miesiąc"

# =============================================
# kategorie
# =============================================
kategorie = {
    "Wpływy": ["500+", "Odsetki", "Premia", "Wynagrodzenie", "Wypłata kredytu", "Wpływy - inne"]
}


# =============================================
# Wpływy Service
# =============================================

class WplywyService:
    def process_wplywy(self, input_file_path):
        xslx = pd.ExcelFile(input_file_path)

        wplywy = []

        for tab in kategorie.keys():
            self.process_category(xslx, tab, wplywy)

        return wplywy

    @staticmethod
    def process_category(xslx, tab, wplywy):
        df = pd.read_excel(xslx, '%s' % tab)

        for index, row in df.iterrows():
            for column in row.keys():
                if column != col_miesiac:
                    w = Wplyw(row[col_miesiac], tab, column, row.get(column))
                    wplywy.append(w)

    def store_wplywy(self, wplywy, database):
        for wplyw in wplywy:
            database.add_wplyw(wplyw.miesiac, wplyw.kategoria, wplyw.subkategoria, wplyw.kwota)
