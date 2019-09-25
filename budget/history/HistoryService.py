import pandas as pd

# =============================================
# constants
# =============================================
from budget.history.HistoryItem import HistoryItem

col_miesiac = "Miesiąc"

# =============================================
# kategorie
# =============================================
wydatki_kategorie = {
    "Auto i transport": ["Akcesoria i eksploatacja", "Paliwo", "Parking i opłaty", "Przejazdy", "Serwis i części",
                         "Ubezpieczenie auta", "Auto i transport - inne"],
    "Codzienne wydatki": ["Alkohol", "Jedzenie poza domem", "Kawa", "Papierosy", "Słodycze i ciasta", "Zwierzęta",
                          "Żywność i chemia domowa", "Codzienne wydatki - inne"],
    "Dom": ["Akcesoria i wyposażenie", "Meble", "Narzędzia", "Remont i ogród", "RTV i AGD", "Ubezpieczenie domu",
            "Usługi domowe", "Dom - inne"],
    "Dzieci": ["Akcesoria dziecięce", "Art. dziecięce i zabawki", "Ciuchy i buty", "Pampersy",
               "Przedszkole i opiekunka", "Szkoła i wyprawka", "Zajęcia dodatkowe", "Dzieci - inne"],
    "Nieskategoryzowane": ["Decoupage + szycie", "Lekarz / apteka", "Wypłata gotówki", "Bez kategorii"],
    "Osobiste": ["Edukacja", "Elektronika", "Multimedia, książki i prasa", "Odzież i obuwie", "Prezenty i wsparcie",
                 "Zdrowie i uroda", "Osobiste - inne"],
    "Płatności": ["Czynsz i wynajem", "Garaż", "Gaz", "Ogrzewanie", "Opłaty i odsetki", "Podatki", "Prąd", "Spłaty rat",
                  "Subskrypcje, abonamenty", "TV, internet, telefon", "Ubezpieczenia", "Woda i kanalizacja",
                  "Płatności - inne"],
    "Rozrywka": ["Podróże i wyjazdy", "Sport i hobby", "Wyjścia i wydarzenia", "Rozrywka - inne"]
}

wplywy_kategorie = {
    "Wpływy": ["500+", "Odsetki", "Premia", "Wynagrodzenie", "Wypłata kredytu", "Wpływy - inne"]
}


# =============================================
# History Service
# =============================================

class HistoryService:
    def process_items(self, input_file_path, kategorie, typ):
        xslx = pd.ExcelFile(input_file_path)

        items = []

        for tab in kategorie.keys():
            self.process_category(xslx, tab, items, typ)

        return items

    @staticmethod
    def process_category(xslx, tab, items, typ):
        df = pd.read_excel(xslx, '%s' % tab)

        for index, row in df.iterrows():
            for column in row.keys():
                if column != col_miesiac:
                    w = HistoryItem(typ, row[col_miesiac], tab, column, row.get(column))
                    items.append(w)

    def store_wydatki(self, wydatki, database):
        for wydatek in wydatki:
            database.add_wydatek(wydatek.miesiac, wydatek.kategoria, wydatek.subkategoria, wydatek.kwota)

    def process_miesiace(self, database):
        return database.select_data(
            "SELECT DISTINCT miesiac FROM wydatki UNION SELECT DISTINCT miesiac FROM wplywy ORDER BY 1 DESC")

    def process_kategorie(self, database):
        return database.select_data("SELECT DISTINCT kategoria FROM wydatki ORDER BY 1 ASC")

    def process_subkategorie(self, database):
        return database.select_data("SELECT DISTINCT kategoria, subkategoria FROM wydatki ORDER BY 1 ASC, 2 ASC")

    def process_sum_wydatki(self, database):
        return database.select_data("SELECT miesiac, SUM(kwota) [suma] FROM wydatki GROUP BY miesiac ORDER BY 1 DESC")

    def process_wydatki_vs_wplywy(selfself, database):
        return database.select_data("SELECT x.miesiac, x.typ, SUM(x.kwota) [suma] FROM (SELECT 'Wpływy' [typ], miesiac, kwota FROM wplywy UNION SELECT 'Wydatki' [typ], miesiac, kwota FROM wydatki) x GROUP BY x.miesiac, x.typ ORDER BY 1 DESC, 2 ASC")

    def store_wplywy(self, wplywy, database):
        for wplyw in wplywy:
            database.add_wplyw(wplyw.miesiac, wplyw.kategoria, wplyw.subkategoria, wplyw.kwota)

    def process_sum_wplywy(self, database):
        return database.select_data("SELECT miesiac, SUM(kwota) [suma] FROM wplywy GROUP BY miesiac ORDER BY 1 DESC")
