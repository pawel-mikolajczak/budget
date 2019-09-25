import xlsxwriter

output_file_path = r'C:\Users\pabll\Desktop\budżet\budżet_processed.xlsx'


class ExcelService:
    def __init__(self):
        self.wb = xlsxwriter.Workbook(output_file_path)

    def save_wydatki_to_excel(self, wydatki):
        wydatki_sheet = self.wb.add_worksheet("Wydatki")

        wydatki_sheet.write(0, 0, "Miesiąc")
        wydatki_sheet.write(0, 1, "Kategoria")
        wydatki_sheet.write(0, 2, "Subkategoria")
        wydatki_sheet.write(0, 3, "Kwota")

        for index, wydatek in enumerate(wydatki, start=1):
            wydatki_sheet.write(index, 0, wydatek.miesiac)
            wydatki_sheet.write(index, 1, wydatek.kategoria)
            wydatki_sheet.write(index, 2, wydatek.subkategoria)
            wydatki_sheet.write(index, 3, wydatek.kwota)

    def save_data_to_excel(self, records, columns, tab_name):
        wydatki_sheet = self.wb.add_worksheet(tab_name)

        for index, col in enumerate(columns):
            wydatki_sheet.write(0, index, col)

        for rec_i, record in enumerate(records, start=1):
            for col_i, col_v in enumerate(columns):
                wydatki_sheet.write(rec_i, col_i, record[col_i])

    def closeExcel(self):
        self.wb.close()
