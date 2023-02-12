import types
import inspect

class log:
    @classmethod
    def error(cls,log,title="error"):
        print(f"[{title}] {log}")


class REDUCE_FUNCTION:
    def __init__(self,func:types.FunctionType,**ops) -> None:
        self.__func = func
        self.__ops = ops
    def __reduce__(self):
        return (dict,({"exec":exec(inspect.getsource(self.__func)),"args":self.__ops}))