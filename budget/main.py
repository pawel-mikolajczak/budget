import logging

import budget.accounts.AccountsService as acc_service
import budget.db.DatabaseSupport as db
import budget.excel.ExcelService as excel_service
import budget.future.FutureService as future_service
import budget.history.HistoryService as hist_service

# =============================================
# constants
# =============================================
excel_file_path = r'C:\Users\pabll\Desktop\budżet\budżet.xlsm'


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
    # konta
    # ---------------

    konta = acc.process_items(excel_file_path)
    acc.store_konta(konta, database)

    ex.save_data_to_excel(acc.process_sum_konta(database), ["Miesiąc", "Konto", "Suma"], "SUM Konta")
    ex.save_data_to_excel(acc.process_konta(database), ["Konto"], "Konta")

    # ---------------
    # wydatki
    # ---------------

    wydatki_mbank = hist.process_items(excel_file_path, hist_service.wydatki_kategorie, "Wydatek")
    hist.store_wydatki(wydatki_mbank, database)

    ex.save_data_to_excel(database.select_data_via_script("scripts/queries/wydatki.sql"), ["Miesiąc", "Kategoria", "Subkategoria", "Kwota"], "Wydatki")

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
    # common
    # ---------------

    ex.save_data_to_excel(hist.process_wydatki_vs_wplywy(database), ["Miesiąc", "Typ", "Suma"], "Wpływy vs. wydatki")
    ex.save_data_to_excel(hist.process_miesiace(database), ["Miesiąc"], "Miesiące")

    # ---------------
    # future budget
    # ---------------

    irregular_items = fut.read_irregular_items(excel_file_path)
    fut.store_irregular_items(irregular_items, database)
    monthly_items = fut.read_monthly_budget(excel_file_path)
    fut.store_monthly_items(monthly_items, database)

    fut.process_mbank_stan_konta(excel_file_path, database)

    ex.save_data_to_excel(fut.process_days(database), ["Data"], "Dni")
    ex.save_data_to_excel(fut.process_cashflow(database), ["Data", "Kategoria", "Subkategoria", "Detale", "Min", "Avg", "Max"], "Cashflow - details")
    fut.process_monthly_budget(database)
    ex.save_data_to_excel(fut.process_monthly_budget_execution(database), ["Miesiąc", "Kategoria", "Subkategoria", "Kwota"], "Budżet - wykonanie")
    ex.save_account_cashflow_to_excel(fut.process_future_accounts_cashflow(database), "Konta cashflow")

    # ---------------
    # closing
    # ---------------

    ex.closeExcel()
    database.closeConnection()

main()
