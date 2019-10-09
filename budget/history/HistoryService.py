import logging

import pandas as pd

from budget.db.DatabaseSupport import DatabaseSupport
from budget.history.HistoryItem import HistoryItem

logger = logging.getLogger("HistoryService")

# =============================================
# constants
# =============================================

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

wydatki_kategorie_pivot = {
    "Rachunki comiesięczne": ["Czynsz i wynajem", "Garaż", "Gaz", "Ogrzewanie", "Prąd", "Spłaty rat",
                              "Subskrypcje, abonamenty", "TV, internet, telefon", "Ubezpieczenia",
                              "Woda i kanalizacja", "Przedszkole i opiekunka", "Zajęcia dodatkowe"],
    "Rachunki inne": ["Opłaty i odsetki", "Podatki", "Ubezpieczenia", "Płatności - inne", "Ubezpieczenie domu"],
    "Życie codzienne": ["Jedzenie poza domem", "Kawa", "Zwierzęta", "Żywność i chemia domowa",
                        "Codzienne wydatki - inne"],
    "Życie zachcianki": ["Alkohol", "Papierosy", "Słodycze i ciasta", "Wyjścia i wydarzenia", "Rozrywka - inne"],
    "Auto comiesięczne": ["Akcesoria i eksploatacja", "Paliwo", "Parking i opłaty", "Przejazdy",
                          "Auto i transport - inne"],
    "Auto co roku": ["Serwis i części", "Ubezpieczenie auta"],
    "Dzieci stałe": ["Akcesoria dziecięce", "Pampersy"],
    "Dzieci zachcianki": ["Art. dziecięce i zabawki"],
    "Dzieci nieprzewidziane": ["Szkoła i wyprawka", "Dzieci - inne"],
    "Sport i hobby": ["Decoupage + szycie", "Sport i hobby"],
    "Zdrowie i uroda": ["Lekarz / apteka", "Zdrowie i uroda"],
    "Inne": ["Wypłata gotówki", "Bez kategorii"],
    "Podróże": ["Podróże i wyjazdy"],
    "Ubrania i obuwie": ["Ciuchy i buty", "Odzież i obuwie"],
    "Prezenty": ["Prezenty i wsparcie"],
    "Osobiste": ["Edukacja", "Multimedia, książki i prasa", "Osobiste - inne"],
    "Elektronika": ["Elektronika", "RTV i AGD"],
    "Dom": ["Akcesoria i wyposażenie", "Meble", "Narzędzia", "Remont i ogród", "Usługi domowe", "Dom - inne"]
}


# =============================================
# History Service
# =============================================

class HistoryService:
    def process_items(self, input_file_path, kategorie, typ):
        xslx = pd.ExcelFile(input_file_path)

        items = list()

        for tab in kategorie.keys():
            logger.info("Processing category '{}' started...".format(tab))
            history = self.process_category(xslx, tab, typ)
            items.extend(history)
            logger.info("Processed {} items for category '{}'".format(history.__len__(), tab))

        return items

    @staticmethod
    def process_category(xslx, tab, typ):
        df = pd.read_excel(xslx, '%s' % tab)

        history = list()

        for index, row in df.iterrows():
            for column in row.keys():
                if column != col_miesiac:
                    w = HistoryItem(typ, row[col_miesiac], tab, column, row.get(column))
                    history.append(w)

        return history

    def store_wydatki(self, wydatki, database: DatabaseSupport):
        for wydatek in wydatki:
            query = "INSERT INTO wydatki ('miesiac', 'kategoria', 'subkategoria', 'kwota') VALUES ('{}','{}','{}',{})".format(
                wydatek.miesiac, wydatek.kategoria, wydatek.subkategoria, wydatek.kwota)
            database.insert_data(query, "Wydatek")

    def process_miesiace(self, database:DatabaseSupport):
        database.select_data_via_script("scripts/queries/process_miesiace.sql")
        return database.select_data("SELECT DISTINCT miesiac FROM miesiace ORDER BY 1 DESC")

    def process_kategorie(self, database):
        return database.select_data("SELECT DISTINCT kategoria FROM wydatki ORDER BY 1 ASC")

    def process_subkategorie(self, database):
        return database.select_data("SELECT DISTINCT kategoria, subkategoria FROM wydatki ORDER BY 1 ASC, 2 ASC")

    def process_sum_wydatki(self, database):
        return database.select_data("SELECT miesiac, SUM(kwota) [suma] FROM wydatki GROUP BY miesiac ORDER BY 1 DESC")

    def process_wydatki_vs_wplywy(self, database):
        return database.select_data(
            "SELECT x.miesiac, x.typ, SUM(x.kwota) [suma] "
            "FROM "
            "   ("
            "       SELECT 'Wpływy' [typ], miesiac, kwota "
            "       FROM wplywy "
            "       UNION "
            "       SELECT 'Wydatki' [typ], miesiac, kwota "
            "       FROM wydatki"
            "   ) x "
            "GROUP BY x.miesiac, x.typ "
            "ORDER BY 1 DESC, 2 ASC")

    def store_wplywy(self, wplywy, database: DatabaseSupport):
        for wplyw in wplywy:
            query = "INSERT INTO wplywy ('miesiac', 'kategoria', 'subkategoria', 'kwota') VALUES ('{}','{}','{}',{})".format(
                wplyw.miesiac, wplyw.kategoria, wplyw.subkategoria, wplyw.kwota)
            database.insert_data(query, "Wpływ")

    def process_sum_wplywy(self, database):
        return database.select_data("SELECT miesiac, SUM(kwota) [suma] "
                                    "FROM wplywy "
                                    "GROUP BY miesiac "
                                    "ORDER BY 1 DESC")

    def process_wydatki_pivot(self, database):
        wydatki = list()

        for cat in wydatki_kategorie_pivot.keys():
            kategoria = cat
            subkategorie = "','".join(wydatki_kategorie_pivot.get(cat))
            query = "SELECT '{}' [kategoria], miesiac, SUM(kwota) [suma] " \
                    "FROM wydatki " \
                    "WHERE subkategoria IN ('{}') " \
                    "GROUP BY miesiac".format(
                kategoria, subkategorie)
            wydatki += database.select_data(query)
            wydatki
        return wydatki
