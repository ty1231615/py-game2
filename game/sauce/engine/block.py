import pygame
from .. import PAK, cash

class Block(PAK.Package):
    #block index
    air = 0
    stone = 1
    goal = 2
    barria = 999
    defalt = 0
    INDEXS = {
        air:"・",
        stone:"■",
        goal:"◆",
        barria:"■"
    }
    def __init__(self,id=defalt,cash={}) -> None:
        super().__init__()
        #blockId can search block by id
        self.__id = id
        self.__cash = cash
    @property
    def package(self):
        return (self.__id,self.__cash)
    @property
    def id(self):
        return self.__id
    @property
    def cash(self):
        return self.__cash
    @cash.setter
    def cash(self,value):
        if isinstance(value,dict):
            self.__cash = value
    def __reduce_ex__(self,prot):
        return (tuple,(tuple((self.package_id,self.__id,self.__cash))))
    def draw(self,screen:pygame.Surface,font:pygame.font.Font,color,x,y):
        #block rendering
        text = Block.INDEXS[self.__id]
        render = font.render(text,True,color)
        screen.blit(render,(x,y))
        return font.size(text)
    def go(self):
        if self.__id == Block.air:
            return True
        if self.__id == Block.barria:
            return False
    def set_attribute(self,key,value):
        #able to add attribute
        #attribute is useful because use when you need any data
        self.__cash.update(
            {key:value}
        )
    def get_attribute(self,value):
        #able to attribute
        return self.__cash.get(value)
    def get_id(self):
        return self.__id

PAK.Package.BLOCK_HANDLER = Block