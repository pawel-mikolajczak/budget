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

    def process_miesiace(self, wydatki):
        miesiace = set()
        for item in wydatki:
            miesiace.add(item.miesiac)
        return miesiace

    def save_miesiace_to_excel(self, wydatki_miesiace, wb):
        wydatki_sheet = wb.add_worksheet("Miesiące")

        wydatki_sheet.write(0, 0, "Miesiąc")

        for index, miesiac in enumerate(wydatki_miesiace, start=1):
            wydatki_sheet.write(index, 0, miesiac)
