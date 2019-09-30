import logging
from typing import List

import pandas as pd

from budget.db.DatabaseSupport import DatabaseSupport
from budget.future.IrregularItem import IrregularItem

DAYS_IN_A_FUTURE = 365*3

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

    def store_irregular_items(self, items: List[IrregularItem], database: DatabaseSupport):
        logger.info("Storing irregular items to database: {}...".format(items.__len__()))
        for item in items:
            query = "INSERT INTO nieregularne ('data', 'kategoria', 'subkategoria', 'detale', 'minimum', 'average', 'maximum', 'finally_paid', 'final_paid_date', 'comments') VALUES ('{}','{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                item.data, item.kategoria, item.subkategoria, item.detale, item.minimum, item.avg, item.maximum,
                item.finally_paid, item.final_paid_date, item.comment)
            database.insert_data(query, "Irregular item")
        logger.info("Storing irregular items to database finished: {}...".format(items.__len__()))

    def process_days(self):
        l = list()
        days = pd.date_range(pd.datetime.today().date(), periods=DAYS_IN_A_FUTURE, freq='D').tolist()
        for day in days:
            x = list()
            x.append(day)
            l.append(x)
        return l
