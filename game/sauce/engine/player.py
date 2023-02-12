import pygame

from . import scene,map,color,gui
from .. import cash

class Player(scene._Scene_obj):
    def __init__(self, x, y,MAP:map.NormalMap,font,mx=0,my=0,color=color.green) -> None:
        super().__init__(self, 0, 0)
        self.__name = "User"
        self.__map = MAP
        self.__scene = None
        self.__color = color
        self.__PLAYER = "▲"
        self.__mx = mx
        self.__my = my
        self.__font = font
    def package_update(self,mx,my,name,text):
        self.__mx = mx
        self.__my = my
        self.__name = name
        self.__PLAYER = text
    @property
    def package(self):
        return (self.__mx,self.__my,self.__name,self.__PLAYER)
    @property
    def text(self):
        return self.__PLAYER
    @property
    def font(self):
        return self.__font
    @font.setter
    def font(self,value):
        if isinstance(value,pygame.font.Font):
            self.__font = value
    @property
    def Color(self):
        return self.__color
    @property
    def Scene(self):
        return self.__scene
    def load(self,scene:scene.Scene):
        self.__scene = scene
        scene.event.KeyBind(self,[pygame.K_UP,pygame.K_w],self.up)
        scene.event.KeyBind(self,[pygame.K_DOWN,pygame.K_s],self.down)
        scene.event.KeyBind(self,[pygame.K_RIGHT,pygame.K_d],self.right)
        scene.event.KeyBind(self,[pygame.K_LEFT,pygame.K_a],self.left)
    def up(self):
        if self.__map.move(self.__mx,self.__my - 1):
            self.__my -= 1
    def down(self):
        if self.__map.move(self.__mx,self.__my + 1):
            self.__my += 1
    def right(self):
        if self.__map.move(self.__mx + 1,self.__my):
            self.__mx += 1
    def left(self):
        if self.__map.move(self.__mx - 1,self.__my):
            self.__mx -= 1
    def draw(self,scene:gui.Surface):
        x,y = self.__map.location(self.__mx,self.__my)
        x -= self.__map.pad / 2
        render = self.__font.render(self.__PLAYER,True,self.__color)
        scene.get_screen().blit(render,(x,y))
        return self.__font.size(self.__PLAYER)
    @property
    def map(self):
        return self.__map
    @property
    def name(self):
        return self.__name
    @property
    def mx(self):
        return self.__mx
    @property
    def my(self):
        return self.__my