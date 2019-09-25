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

    ws.save_wydatki_to_excel(wydatki, wb)
    ws.save_miesiace_to_excel(wydatki_miesiace, wb)

    wb.close()
    database.closeConnection()


main()
