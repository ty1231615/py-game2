import pygame
import socket
from . import scene,map,gui,color
from .. import PAK, approach,cash

class Enemy(scene._Scene_obj):
    def __init__(self,MAP:map.NormalMap,mx,my,size=30,color=color.red) -> None:
        super().__init__(self, 0, 0)
        self.__map = MAP
        self.__color = color
        self.__mx = mx
        self.__my = my
        self.__AI = AI_TYPE.Normal
        self.__text = "▲"
        self.__font = pygame.font.Font(cash.font_path,size)
    def package_update(self,mx,my,text):
        self.__mx = mx
        self.__my = my
        self.__text = text
    @property
    def package(self):
        return (self.__mx,self.__my,self.__text,self.__AI)
    def draw(self,scene:gui.Surface):
        x,y = self.__map.location(self.__mx,self.__my)
        x -= self.__map.pad / 2
        render = self.__font.render(self.__text,True,self.__color)
        scene.get_screen().blit(render,(x,y))
        return self.__font.size(self.__text)
    def __reduce_ex__(self, __protocol):
        return (eval("Package.ENEMY_HANDLER"),(self.package_id,self.map,self.mx,self.my),None,None,None)
    @property
    def map(self):
        return self.__map
    @property
    def mx(self):
        return self.__mx
    @property
    def my(self):
        return self.__my
    @property
    def text(self):
        return self.__text
    @property
    def id(self):
        return self.__id

class AI_TYPE:
    Normal = "ENEMY.AI.NOR1"

PAK.Package.ENEMY_HANDLER = Enemy