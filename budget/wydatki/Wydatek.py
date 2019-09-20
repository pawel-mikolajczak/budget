from datetime import datetime


class Wydatek:
    def __init__(self, miesiac, kategoria, subkategoria, kwota):
        self.miesiac = miesiac
        self.kategoria = kategoria
        self.subkategoria = subkategoria
        self.kwota = kwota
        print("Wydatek init {}, {}, {}, {}".format(miesiac, kategoria, subkategoria, kwota))

    def __str__(self) -> str:
        return "Miesiąc={}; Kategoria={}; Subkategoria={}; Kwota={}".format(self.get_miesiac_as_date(), self.kategoria,
                                                                            self.subkategoria, self.kwota)

    def __repr__(self) -> str:
        return self.__str__()

    def get_miesiac_as_date(self) -> datetime:
        return datetime.strptime(str(self.miesiac), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
