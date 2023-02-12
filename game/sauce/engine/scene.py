import pygame
import types

from . import gui,color,system,collide
from .. import PAK

class _Scene_obj(PAK.Package):
    def __init__(self,obj,x,y) -> None:
        super().__init__()
        self.__obj = obj
        self.__x = x
        self.__y = y
    def load(self,scene):
        return True
    def set_pos(self,x,y):
        self.__x = x
        self.__y = y
    def draw(self):
        return
    def get_defalt_pos(self):
        return (self.__x,self.__y)
    def true_pos(self,x,y):
        return (self.__x + x,self.__y + y)
    def fit(self):
        return False
    def get_obj(self):
        return self.__obj

class Scene:
    def __init__(self,screen:gui.Surface,size=None,background=color.black) -> None:
        self.__cog = system.Cog()
        self.x = 0
        self.y = 0
        self._screen = screen
        self.size = size
        self.__background = background
        self.__objs = []
        self.__define = []
        self.__collider = collide.Collider()
        self.__event = collide.Event()
        #patch datas
        self.__cog.patch("x",lambda: self.x)
        self.__cog.patch("y",lambda: self.y)
        self.__cog.patch("screen",lambda: self._screen)
        self.__cog.patch("size",lambda: self.size)
        self.__cog.patch("background",lambda: self.background)
        self.__cog.patch("objs",lambda: self.__objs)
        self.__cog.patch("define",lambda: self.__define)
    @property
    def collider(self):
        return self.__collider
    @property
    def event(self):
        return self.__event
    @property
    def background(self):
        return self.__background
    @background.setter
    def background(self,value:tuple):
        if isinstance(value,tuple):
            self.__background = value
    @property
    def cog(self):
        return self.__cog
    def set_defalt_pos(self,x,y):
        self.x=x
        self.y=y
    def regit(self,*objs:_Scene_obj):
        for i in objs:
            self.__objs.append(i)
    def cog_regit(self,**objs):
        for name in objs:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
            self.__objs.append(objs[name])
            self.cog.patch(
                name,
                objs[name]
            )
    def regit_def(self,*func:types.FunctionType):
        for i in func:
            self.__define.append(func)
    def load(self):
        if self.size:
            self._screen.resize(self.size)
        for obj in self.__objs:
            obj.load(self)
        for func in self.__define:
            func(self.cog)
    def draw(self):
        for i in self.__objs:
            i.set_pos(self.x,self.y)
            i.draw(self._screen)


