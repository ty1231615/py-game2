import tkinter as tk
import pygame
from pygame.locals import *
import sys
import random

from . import animation
from .account import LOGIN_CANVAS,AccountCreateCanvas
from . import command
from . import approach
from . import cash
from .engine import button,collide,scene,gui,color,session

class GUI:
    def __init__(self) -> None:
        self.__SIZE_X = 1000
        self.__SIZE_Y = 600
    def get_size(self):
        return (self.__SIZE_X,self.__SIZE_Y)
    def init_gui(self):
        self.root = tk.Tk()
        self.root.title("R E C U B E")
        self.root.geometry(f"{self.__SIZE_X}x{self.__SIZE_Y}")
        self.root.resizable(0,0)
        #self.root.attributes("-fullscreen",True)
    def setup_login(self):
        self.create_login = AccountCreateCanvas(self.root)
        self.create_login.place(x=-self.__SIZE_X,relheight=1,relwidth=1)
        self.login = LOGIN_CANVAS(self.root)
        def SlideLoginCanvas():
            plot = animation.easing.TotalInExpo(50,0,0.02,0,self.__SIZE_X,1)
            plot2 = animation.easing.TotalInExpo(50,0,0.02,0,self.__SIZE_X,1)
            self.create_login.setup(lambda: load_main())
            animation.easing.easing_canvas(self.login,plot,[0],100)
            animation.easing.easing_canvas(self.create_login,plot2,[0],10)
        def load_main():
            self.create_login.destroy()
            self.login.destroy()
            cash._root.destroy()
        self.login.place(relheight=1,relwidth=1)
        self.login.setup(create_account=SlideLoginCanvas,login=load_main)
    def run(self):
        self.root.mainloop()

class EngineGUI:
    def __init__(self,width,height,server:approach.DataServerHandler ) -> None:
        self.__screen = gui.Surface(width,height)
        self.__now_scene = scene.Scene(self.__screen)
        self.__run = False
        self.__server = server
    @property
    def server(self):
        return self.__server
    @property
    def Scene(self):
        return self.__now_scene
    @property
    def sessions(self):
        return self.__sessions
    def get_screen(self) -> gui.Surface:
        return self.__screen
    def startup(self):
        pygame.init()
        self.__screen.setup()
        print(self.__screen)
        pygame.display.set_caption("R E C U B E")
    def set_load_scene(self,scn:scene.Scene):
        if isinstance(scn,scene.Scene):
            print(f"loaded {scn}")
            scn.load()
            self.__now_scene = scn
    def run(self):
        self.__run = True
        while self.__run:
            pygame.display.update()
            self.__screen.get_screen().fill(self.__now_scene.background)
            self.__now_scene.draw()
            self.event_controle()
            if self.__run:
                pygame.display.update()
    def event_controle(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                self.__run = False
                cash.exit()
                return
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for i in self.__now_scene.collider.GetMouseClick:
                    if i.get_obj().collidepoint(event.pos):
                        i.get_func()()
            if event.type == KEYDOWN:
                for i in self.__now_scene.event.GetKeyBind:
                    if event.key in i.attribute["key"]:
                        i.get_func()()
        for i in self.__now_scene.collider.GetMouseCollider:
            if i.get_obj().collidepoint(pygame.mouse.get_pos()):
                i.get_func()[0]()
            else:
                i.get_func()[1]()
    def get_width(self):
        return self.__width
    def get_height(self):
        return self.__height