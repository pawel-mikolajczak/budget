import budget.db.DatabaseSupport as db
import budget.wydatki.WydatkiService as wyd_service
import budget.wplywy.WplywyService as wpl_service
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
    # ---------------
    # init services
    # ---------------

    wyd = wyd_service.WydatkiService()
    wpl = wpl_service.WplywyService()
    ex = excel_service.ExcelService()

    # ---------------
    # database
    # ---------------

    database = db.DatabaseSupport()
    database.initDatabase()

    # ---------------
    # wydatki
    # ---------------

    wydatki = wyd.process_wydatki(excel_file_path)
    wyd.store_wydatki(wydatki, database)

    ex.save_item_to_excel(wydatki, "Wydatki")

    ex.save_data_to_excel(wyd.process_kategorie(database), ["Kategoria"], "Kategorie")
    ex.save_data_to_excel(wyd.process_subkategorie(database), ["Kategoria", "Subkategoria"], "Subkategorie")
    ex.save_data_to_excel(wyd.process_sum_wydatki(database), ["Miesiąc", "Suma"], "Wydatki SUM")

    # ---------------
    # wplywy
    # ---------------

    wplywy = wpl.process_wplywy(excel_file_path)
    wpl.store_wplywy(wplywy, database)

    ex.save_item_to_excel(wplywy, "Wpływy")

    # ---------------
    # common
    # ---------------

    ex.save_data_to_excel(wyd.process_miesiace(database), ["Miesiąc"], "Miesiące")

    # ---------------
    # closing
    # ---------------

    ex.closeExcel()
    database.closeConnection()


main()
