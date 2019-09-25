import pandas as pd

# =============================================
# constants
# =============================================
from budget.wydatki.Wydatek import Wydatek

col_miesiac = "Miesiąc"

# =============================================
# kategorie
# =============================================
kategorie = {
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


# =============================================
# Wydatki Service
# =============================================

class WydatkiService:
    def process_wydatki(self, input_file_path):
        xslx = pd.ExcelFile(input_file_path)

        wydatki = []

        for tab in kategorie.keys():
            self.process_category(xslx, tab, wydatki)

        return wydatki

    @staticmethod
    def process_category(xslx, tab, wydatki):
        df = pd.read_excel(xslx, '%s' % tab)

        for index, row in df.iterrows():
            for column in row.keys():
                if column != col_miesiac:
                    w = Wydatek(row[col_miesiac], tab, column, row.get(column))
                    wydatki.append(w)

    def save_wydatki_to_excel(self, wydatki, wb):
        wydatki_sheet = wb.add_worksheet("Wydatki")

        wydatki_sheet.write(0, 0, "Miesiąc")
        wydatki_sheet.write(0, 1, "Kategoria")
        wydatki_sheet.write(0, 2, "Subkategoria")
        wydatki_sheet.write(0, 3, "Kwota")

        for index, wydatek in enumerate(wydatki, start=1):
            wydatki_sheet.write(index, 0, wydatek.miesiac)
            wydatki_sheet.write(index, 1, wydatek.kategoria)
            wydatki_sheet.write(index, 2, wydatek.subkategoria)
            wydatki_sheet.write(index, 3, wydatek.kwota)

    def process_miesiace(self, database):
        return database.select_data("SELECT DISTINCT miesiac FROM wydatki ORDER BY 1 DESC")

    def process_kategorie(self, database):
        return database.select_data("SELECT DISTINCT kategoria FROM wydatki ORDER BY 1 ASC")

    def process_subkategorie(self, database):
        return database.select_data("SELECT DISTINCT kategoria, subkategoria FROM wydatki ORDER BY 1 ASC, 2 ASC")

    def process_sum_wydatki(self, database):
        return database.select_data("SELECT miesiac, SUM(kwota) [suma] FROM wydatki GROUP BY miesiac ORDER BY 1 DESC")

    def save_data_to_excel(self, records, columns, tab_name, wb):
        wydatki_sheet = wb.add_worksheet(tab_name)

        for index, col in enumerate(columns):
            wydatki_sheet.write(0, index, col)

        for rec_i, record in enumerate(records, start=1):
            for col_i, col_v in enumerate(columns):
                wydatki_sheet.write(rec_i, col_i, record[col_i])

    def store_wydatki(self, wydatki, database):
        for wydatek in wydatki:
            database.add_wydatek(wydatek.miesiac, wydatek.kategoria, wydatek.subkategoria, wydatek.kwota)
