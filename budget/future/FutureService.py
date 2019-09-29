import pandas as pd

from budget.future.IrregularItem import IrregularItem

import logging

logger = logging.getLogger("FutureService")

# =============================================
# constants
# =============================================

# =============================================
# future_tabs
# =============================================
irregular_tab = "B - Nieregularne"


# =============================================
# Future Service
# =============================================

class FutureService:
    def read_irregular_items(self, input_file_path):
        xslx = pd.ExcelFile(input_file_path)

        items = []

        df = pd.read_excel(xslx, '%s' % irregular_tab)

        for index, row in df.iterrows():
            i = IrregularItem(row["Data"], row["Kategoria"], row["Podkategoria"], row["Detale"], row["Minimum"],
                              row["AVG"], row["Maximum"], row["Finalnie zapłacono"], row["Finalna data zakupu"],
                              row["Komentarz"])
            items.append(i)

        return items
