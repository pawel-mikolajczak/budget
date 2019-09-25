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

    ex.save_wydatki_to_excel(wydatki)
    ex.save_data_to_excel(ws.process_miesiace(database), ["Miesiąc"], "Miesiące")
    ex.save_data_to_excel(ws.process_kategorie(database), ["Kategoria"], "Kategorie")
    ex.save_data_to_excel(ws.process_subkategorie(database), ["Kategoria", "Subkategoria"], "Subkategorie")
    ex.save_data_to_excel(ws.process_sum_wydatki(database), ["Miesiąc", "Suma"], "Wydatki SUM")

    ex.closeExcel()
    database.closeConnection()


main()
