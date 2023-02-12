from pygame.locals import *
import pygame
import types
from . import collide
from . import scene
from . import gui
from . import system
from statistics import mean


#all buttons base class
class ButtonBase(scene._Scene_obj):
    def __init__(self,x,y,x2,y2,text,font:pygame.font.Font,color=(0,0,0),backgroundColor=(255,255,255),func=lambda: print("Hello Guys!")):
        super().__init__(self,0,0)
        self.__text = text
        self.__font = font
        self.__func = func
        self.__color = color
        self.__background_color = backgroundColor
        self.__x = x
        self.__y = y
        self.__x2 = x2
        self.__y2 = y2
        self._vx = x
        self._vy = y
        self.__body = pygame.Rect(self.__x,self.__y,self.__x2,self.__y2)
    def get_body(self):
        return self.__body
    def get_font(self):
        return self.__font
    def get_color(self):
        return self.__color
    def get_background_color(self):
        return self.__background_color
    def set_size(self,x,y,x2,y2):
        self.__x = x
        self.__x2 = x2
        self.__y = y
        self.__y2 = y2
    def get_size(self):
        return (self.__x,self.__y,self.__x2,self.__y2)
    def get_text(self):
        return self.__text
    def load(self,scene:scene.Scene):
        #setting mouse action by Collider class
        scene.collider.MouseClick(self.get_body(),self.__func)
    def fit(self):
        #resize block data
        x,y = self.get_defalt_pos()
        self._vx = self.__x + x
        self._vy = self.__y + y
    def draw(self,screen:gui.Surface):
        screen = screen.get_screen()
        self.fit()
        self.__body.update(self._vx,self._vy,self.__x2,self.__y2)
        render = self.__font.render(self.__text,True,self.__color)
        pygame.draw.rect(screen,self.__background_color,self.__body)
        center = self.__font.size(self.__text)
        screen.blit(render,(self._vx + self.__x2 / 2 - center[0] / 2,self._vy + self.__y2 / 2 - center[1] / 2))

class ScaleButton(ButtonBase):
    def __init__(self, x, y, x2, y2, scale, text, font: pygame.font.Font, color=(0, 0, 0), backgroundColor=(255, 255, 255), delay=0, func=lambda: print("Hello Guys!")):
        super().__init__(x, y, x2, y2, text, font, color, backgroundColor,func=func)
        self.__scale = scale
        self.__delay = delay
        self.__now_scale = 0
        self._defalt_x = x
        self._defalt_y = y
        self._defalt_x2 = x2
        self._defalt_y2 = y2
        self._move_x = x
        self._move_x2 = x2
        self._move_y = y
        self._move_y2 = y2
    def load(self,scene:scene.Scene):
        super().load(scene)
        #mouse action when mouse is colliding setting by Collider class
        #this action is scale up and down
        scene.collider.MouseCollider(self.get_body(),[system.DelayDef(self.scale_up,self.__delay),system.DelayDef(self.scale_down,self.__delay)])
    def scaler(self,scale):
        self._move_x = self._defalt_x - scale / 2
        self._move_y = self._defalt_y - scale / 2
        self._move_x2 = self._defalt_x2 + scale / 2
        self._move_y2 = self._defalt_y2 + scale / 2
        self.set_size(self._move_x,self._move_y,self._move_x2,self._move_y2)
    def scale_up(self):
        if self.__now_scale < self.__scale:
            self.__now_scale += 1
            self.scaler(self.__now_scale)
    def scale_down(self):
        if self.__now_scale > 0:
            self.__now_scale -= 1
            self.scaler(self.__now_scale)
    def get_scale(self):
        return self.__scale

class BlockScaleButton(ScaleButton):
    def __init__(self, x, y, x2, y2, scale, text, font: pygame.font.Font, color=(0, 0, 0), backgroundColor=(255, 255, 255),delay=0,func=lambda: print("Hello Guys!")):
        super().__init__(x, y, x2, y2, scale, text, font, color, backgroundColor,delay,func=func)
    def scaler(self,scale):
        self._move_x = self._defalt_x + scale / 2
        self._move_y = self._defalt_y + scale / 2
        self._move_x2 = self._defalt_x2
        self._move_y2 = self._defalt_y2
        self.set_size(self._move_x,self._move_y,self._move_x2,self._move_y2)
    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        x,y = self.get_defalt_pos()
        size = self.get_size()
        line_size = 1
        pygame.draw.line(screen,self.get_background_color(),(self._defalt_x + x,self._defalt_y + y),(self._defalt_x + size[2] + x,self._defalt_y + y),line_size)
        pygame.draw.line(screen,self.get_background_color(),(self._defalt_x + x,self._defalt_y + y),(self._defalt_x + x,self._defalt_y + size[3] + y),line_size)
        
        pygame.draw.line(screen,self.get_background_color(),(self._defalt_x + x,self._defalt_y + y),(self._move_x + x,self._move_y + y),line_size + 1)
        pygame.draw.line(screen,self.get_background_color(),(self._defalt_x + size[2] + x,self._defalt_y + y),(self._move_x + size[2] + x,self._move_y + y),line_size)
        pygame.draw.line(screen,self.get_background_color(),(self._defalt_x + x,self._defalt_y + size[3] + y),(self._move_x + x,self._move_y + size[3] + y),line_size + 1)

class FadeCarcle(scene._Scene_obj):
    def __init__(self,color,WH,size) -> None:
        super().__init__(self,WH[0],WH[1])
        self.color = color
        self.wh = WH
        self.defo = size
        self.size = size
        self.mode = 1
    def draw(self,screen:gui.Surface):
        screen = screen.get_screen()
        x,y = self.get_defalt_pos()
        pygame.draw.circle(screen,self.color,(self.wh[0] + x,self.wh[1] + y),self.size)
        if self.mode:
            self.size -= 1
        else:
            self.size += 1
        if self.size <= 0:
            self.mode = 0
        elif self.size > self.defo:
            self.mode = 1