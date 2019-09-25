import budget.db.DatabaseSupport as db
import budget.history.HistoryService as hist_service
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

    hist = hist_service.HistoryService()
    ex = excel_service.ExcelService()

    # ---------------
    # database
    # ---------------

    database = db.DatabaseSupport()
    database.initDatabase()

    # ---------------
    # wydatki
    # ---------------

    wydatki = hist.process_items(excel_file_path, hist_service.wydatki_kategorie, "Wydatek")
    hist.store_wydatki(wydatki, database)

    ex.save_item_to_excel(wydatki, "Wydatki")

    ex.save_data_to_excel(hist.process_kategorie(database), ["Kategoria"], "Kategorie")
    ex.save_data_to_excel(hist.process_subkategorie(database), ["Kategoria", "Subkategoria"], "Subkategorie")
    ex.save_data_to_excel(hist.process_sum_wydatki(database), ["Miesiąc", "Suma"], "Wydatki SUM")

    # ---------------
    # wplywy
    # ---------------

    wplywy = hist.process_items(excel_file_path, hist_service.wplywy_kategorie, "Wpływ")
    hist.store_wplywy(wplywy, database)

    ex.save_item_to_excel(wplywy, "Wpływy")
    ex.save_data_to_excel(hist.process_sum_wplywy(database), ["Miesiąc", "Suma"], "Wpływy SUM")

    # ---------------
    # common
    # ---------------

    ex.save_data_to_excel(hist.process_wydatki_vs_wplywy(database), ["Miesiąc", "Typ", "Suma"], "Wpływy vs. wydatki")
    ex.save_data_to_excel(hist.process_miesiace(database), ["Miesiąc"], "Miesiące")

    # ---------------
    # closing
    # ---------------

    ex.closeExcel()
    database.closeConnection()


main()
