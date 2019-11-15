import xlsxwriter

import logging

logger = logging.getLogger("ExcelService")

output_file_path = r'C:\Users\pabll\Desktop\budżet\budżet_processed.xlsx'


class ExcelService:
    def __init__(self):
        self.wb = xlsxwriter.Workbook(output_file_path)

    def save_item_to_excel(self, items, tab_name):
        sheet = self.wb.add_worksheet(tab_name)

        sheet.write(0, 0, "Miesiąc")
        sheet.write(0, 1, "Kategoria")
        sheet.write(0, 2, "Subkategoria")
        sheet.write(0, 3, "Kwota")

        for index, item in enumerate(items, start=1):
            sheet.write(index, 0, item.miesiac)
            sheet.write(index, 1, item.kategoria)
            sheet.write(index, 2, item.subkategoria)
            sheet.write(index, 3, item.kwota)

    def save_data_to_excel(self, records, columns, tab_name):
        wydatki_sheet = self.wb.add_worksheet(tab_name)

        for index, col in enumerate(columns):
            wydatki_sheet.write(0, index, col)

        for rec_i, record in enumerate(records, start=1):
            for col_i, col_v in enumerate(columns):
                wydatki_sheet.write(rec_i, col_i, record[col_i])

    def save_account_cashflow_to_excel(self, items, tab_name):
        sheet = self.wb.add_worksheet(tab_name)

        sheet.write(0, 0, "Konto")
        sheet.write(0, 1, "Miesiąc")
        sheet.write(0, 2, "Min")
        sheet.write(0, 3, "Avg")
        sheet.write(0, 4, "Max")

        for index, item in enumerate(items, start=1):
            sheet.write(index, 0, item.konto)
            sheet.write(index, 1, item.miesiac)
            sheet.write(index, 2, item.min)
            sheet.write(index, 3, item.avg)
            sheet.write(index, 4, item.max)

    def closeExcel(self):
        self.wb.close()
