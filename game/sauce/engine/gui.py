import pygame

class Surface(pygame.Surface):
    def __init__(self,width,height,defalt_x=0,defalt_y=0) -> None:
        super().__init__((width,height))
        self.__width = width
        self.__height = height
        self.__defalt_x = defalt_x
        self.__defalt_y = defalt_y
        self.__surface = None
    def resize(self,size:tuple):
        if self.__surface:
            self.__surface = pygame.display.set_mode(size,pygame.RESIZABLE)
            self.__width = size[0]
            self.__height = size[1]
    def setup(self):
        self.__surface = pygame.display.set_mode((self.__width,self.__height),pygame.RESIZABLE)
    def get_screen(self):
        return self.__surface
    def get_width(self):
        return self.__width
    def get_height(self):
        return self.__height
    def get_defalt_pos(self):
        return (self.__defalt_x,self.__defalt_y)