import types

class DelayDef:
    def __init__(self,func:types.FunctionType,delay:int) -> None:
        self.__func = func
        self.__delay = delay
        self.__now = 0
    def __call__(self):
        if self.__now > self.__delay:
            self.__func()
            self.__now = 0
        else:
            self.__now += 1

class Cog:
    def __init__(self):
        self.__datas = {}
    def patch(self,key,propert:types.FunctionType):
        self.__datas.update(
            {key:lambda: propert}
        )
    def _get_all(self):
        return self.__datas
    def get(self,key):
        return self.__datas.get(key,lambda: None)()
 
class CogDef:
    @classmethod
    def CogDefine(cls):
        def deco(func):
            def warp(*args,**kwargs):
                return func(*args,**kwargs)
            return CogDef(func)
        return deco
    def __init__(self,func:types.FunctionType) -> None:
        self.__func = func
    def __call__(self,cog:Cog):
        self.__args = {}
        for arg in self.__func.__code__.co_varnames[:self.__func.__code__.co_argcount]:
            self.__args.update(
                {
                    arg:cog.get(arg)
                }
            )
        return self.__func(**self.__args)


class Binder:
    def __init__(self,first_argment=None) -> None:
        self.__first_argment = first_argment
        self.__binds = {}
    def get_binds(self):
        return self.__binds
    def action(self,tag):
        return self.__binds.get(tag,lambda  arg:None)(self.__first_argment)
    def bind(self,tag,func:types.FunctionType):
        self.__binds.update(
            {
                tag:func
            }
        )