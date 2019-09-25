import budget.db.DatabaseSupport as db
import budget.wydatki.WydatkiService as wyd_service
import budget.excel.ExcelService as excel_service

# =============================================
# constants
# =============================================
excel_file_path = r'C:\Users\pabll\Desktop\budżet\budżet.xlsx'


# =============================================
# konta
# =============================================
konta = ["K - Inteligo Paweł", "K - Inteligo Agatka", "K - Gotówka PLN", "K - Auto", "K - Poduszka bezpieczeństwa",
         "K - Wakacje", "K - Filip", "K - Tomek", "K - Santander"]


def main():
    ws = wyd_service.WydatkiService()
    ex = excel_service.ExcelService()

    database = db.DatabaseSupport()
    database.initDatabase()

    wydatki = ws.process_wydatki(excel_file_path)
    ws.store_wydatki(wydatki, database)

    wydatki_miesiace = ws.process_miesiace(database)
    wydatki_kategorie = ws.process_kategorie(database)
    wydatki_subkategorie = ws.process_subkategorie(database)
    wydatki_sum = ws.process_sum_wydatki(database)

    ex.save_wydatki_to_excel(wydatki)
    ex.save_data_to_excel(wydatki_miesiace, ["Miesiąc"], "Miesiące")
    ex.save_data_to_excel(wydatki_kategorie, ["Kategoria"], "Kategorie")
    ex.save_data_to_excel(wydatki_subkategorie, ["Kategoria", "Subkategoria"], "Subkategorie")
    ex.save_data_to_excel(wydatki_sum, ["Miesiąc", "Suma"], "Wydatki SUM")

    ex.closeExcel()
    database.closeConnection()


main()
