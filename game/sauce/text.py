from .lang import LangWord

class TextH:
    def __init__(self) -> None:
        self.__values = []
        self.__tag = self.__hash__()
    def GetAll(self):
        return self.__values
    def add(self,name,value:LangWord):
        self.__values.append(
            (f"{self.__tag}{name}",value)
        )
    def IndexGet(self,index):
        try:
            return self.__values.index(index)
        except ValueError:
            return None
    def get(self,name) -> tuple:
        for i in self.__values:
            if i[0] == f"{self.__tag}{name}":
                return i