

class LangWord:
    _base_word = "no messages here ( ¯−¯ )"
    def __init__(self,jp=_base_word,en=_base_word) -> None:
        self.__jp = jp
        self.__en = en
    def jp(self,value):
        self.__jp = value
    def en(self,value):
        self.__en = value
    def __str__(self) -> str:
        return self.__en
    def get(self,lang):
        pattern = {
            "jp":self.__jp,
            "en":self.__en
        }
        return pattern.get(lang,pattern["en"])