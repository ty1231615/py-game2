import pickle

class DATA:
    def __init__(self,type,value) -> None:
        self.__type = type
        self.__value = value
    def get_type(self):
        return self.__type
    def get_value(self):
        return self.__value
    def __reduce__(self):
        return (dict,({"type":self.__type,"value":self.__value},))
    def encode(self):
        return pickle.dumps(self)
    @classmethod
    def ENCODE(cls,data:dict):
        instance = DATA(data["type"],data["value"])
        return instance

def keyFact(obj:dict,keys:list):
    if all(i in obj for i in keys):
        return (True,)
    else:
        return (False,[i in obj for i in keys],[i not in obj for i in keys])

def attrFact(obj,attrs:list):
    if all(i in obj.__dict__ for i in attrs):
        return (True,)
    else:
        return (False,[i for i in attrs if i in obj.__dict__],[i for i in attrs if not i in obj.__dict__])