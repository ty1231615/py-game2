from . import lang
from . import setting

class Langs:
    def __init__(self) -> None:
        self.__langs = []
    def add(self,lang:lang.LangWord):
        self.__langs.append(lang)
    def get(self,index):
        return self.__langs[index]
    def getDefalt(self,index):
        lng:lang.LangWord = self.__langs[index]
        return lng.get(setting.language)