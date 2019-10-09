import logging

import budget.accounts.AccountsService as acc_service
import budget.db.DatabaseSupport as db
import budget.excel.ExcelService as excel_service
import budget.future.FutureService as future_service
import budget.history.HistoryService as hist_service

# =============================================
# constants
# =============================================
excel_file_path = r'C:\Users\pabll\Desktop\budżet\budżet.xlsx'


def main():
    # ---------------
    # logging setup
    # ---------------
    logging.basicConfig(format='%(asctime)s %(levelname)-5s - %(name)-20s: %(message)s', level=logging.DEBUG)

    # ---------------
    # init services
    # ---------------

    hist = hist_service.HistoryService()
    ex = excel_service.ExcelService()
    acc = acc_service.AccountsService()
    fut = future_service.FutureService()

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
    ex.save_data_to_excel(hist.process_wydatki_pivot(database), ["Kategoria", "Miesiąc", "Suma"], "Wydatki pivot SUM")

    # ---------------
    # wplywy
    # ---------------

    wplywy = hist.process_items(excel_file_path, hist_service.wplywy_kategorie, "Wpływ")
    hist.store_wplywy(wplywy, database)

    ex.save_item_to_excel(wplywy, "Wpływy")
    ex.save_data_to_excel(hist.process_sum_wplywy(database), ["Miesiąc", "Suma"], "Wpływy SUM")

    # ---------------
    # konta
    # ---------------

    konta = acc.process_items(excel_file_path)
    acc.store_konta(konta, database)

    ex.save_data_to_excel(acc.process_sum_konta(database), ["Miesiąc", "Konto", "Suma"], "SUM Konta")
    ex.save_data_to_excel(acc.process_konta(database), ["Konto"], "Konta")

    # ---------------
    # common
    # ---------------

    ex.save_data_to_excel(hist.process_wydatki_vs_wplywy(database), ["Miesiąc", "Typ", "Suma"], "Wpływy vs. wydatki")
    ex.save_data_to_excel(hist.process_miesiace(database), ["Miesiąc"], "Miesiące")

    # ---------------
    # future budget
    # ---------------

    irregular_items = fut.read_irregular_items(excel_file_path)
    fut.store_irregular_items(irregular_items, database)

    ex.save_data_to_excel(fut.process_days(database), ["Data"], "Dni")
    ex.save_data_to_excel(fut.process_cashflow(database), ["Data", "Detale", "Min", "Avg", "Max"], "Cashflow - details")

    # ---------------
    # closing
    # ---------------

    ex.closeExcel()
    database.closeConnection()


main()
