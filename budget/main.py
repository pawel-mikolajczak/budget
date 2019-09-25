from xlwt import Workbook
import xlsxwriter

import budget.wydatki.WydatkiService as wyd_service
import budget.db.DatabaseSupport as db

# =============================================
# constants
# =============================================
excel_file_path = r'C:\Users\pabll\Desktop\budżet\budżet.xlsx'
output_file_path = r'C:\Users\pabll\Desktop\budżet\budżet_processed.xlsx'

# =============================================
# konta
# =============================================
konta = ["K - Inteligo Paweł", "K - Inteligo Agatka", "K - Gotówka PLN", "K - Auto", "K - Poduszka bezpieczeństwa",
         "K - Wakacje", "K - Filip", "K - Tomek", "K - Santander"]


def main():
    ws = wyd_service.WydatkiService()

    database = db.DatabaseSupport()
    database.initDatabase()

    wb = xlsxwriter.Workbook(output_file_path)

    wydatki = ws.process_wydatki(excel_file_path)
    ws.store_wydatki(wydatki, database)

    wydatki_miesiace = ws.process_miesiace(database)
    wydatki_kategorie = ws.process_kategorie(database)
    wydatki_subkategorie = ws.process_subkategorie(database)

    ws.save_wydatki_to_excel(wydatki, wb)
    ws.save_miesiace_to_excel(wydatki_miesiace, wb)
    ws.save_kategorie_to_excel(wydatki_kategorie, wb)
    ws.save_subkategorie_to_excel(wydatki_subkategorie, wb)

    wb.close()
    database.closeConnection()


main()
