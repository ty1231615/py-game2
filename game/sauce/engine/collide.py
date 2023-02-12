import types

class _callstack:
    def __init__(self,obj,funcs:list,**args) -> None:
        self.__obj = obj
        self.__funcs = funcs
        self.__args = args
    @property
    def attribute(self):
        return self.__args
    def get_obj(self):
        return self.__obj
    def get_func(self):
        return self.__funcs

#↓ the system controle all collider
class Collider:
    def __init__(self) -> None:
        self.__MOUSE_COLLIDE = []
        self.__MOUSE_CLICK = []
    @property
    def GetMouseCollider(self):
        return self.__MOUSE_COLLIDE
    @property
    def GetMouseClick(self):
        return self.__MOUSE_CLICK
    def MouseCollider(self,obj,func=lambda:None):
        self.__MOUSE_COLLIDE.append(_callstack(obj,func))
    def MouseClick(self,obj,func=lambda: None):
        self.__MOUSE_CLICK.append(_callstack(obj,func))

class Event:
    def __init__(self) -> None:
        self.__KEY_BIND = []
    def KeyBind(self,obj,key:list,func=lambda: None):
        self.__KEY_BIND.append(_callstack(obj,func,key=key))
    @property
    def GetKeyBind(self):
        return self.__KEY_BIND