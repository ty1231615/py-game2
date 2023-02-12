import pygame
from . import scene,block,gui,color
from .. import PAK, cash

class MapBase(scene._Scene_obj):
    def __init__(self,x,y,pad,MAP=[]) -> None:
        super().__init__(self,0,0)
        self.__x = x
        self.__y = y
        self.__pad = pad
        self.map = MAP
    def __reduce_ex__(self,prot):
        print(__file__)
        return (tuple,(tuple((self.package_id,self.__pad,self.map))))
    @property
    def package(self):
        pack_map = []
        for y in self.map:
            line = []
            for x in y:
                line.append(x.package)
            pack_map.append(line)
        return pack_map
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    @property
    def pad(self):
        return self.__pad
    def draw(self):
        return self.get_defalt_pos()
    def move(self,x,y):
        return self.map[y][x].go()
    def setup(self,size:tuple):
        self.map = [[block.Block() for _ in range(size[0])] for i in range(size[1])]
        print(len(self.map[0]),len(self.map))


class NormalMap(MapBase):
    def __init__(self, x, y, pad, size) -> None:
        super().__init__(x, y, pad)
        self.__size = size
    @property
    def size(self):
        return self.__size
    @size.setter
    def size(self,value):
        if isinstance(value,int):
            self.__size = value
    def location(self,x,y):
        dx,dy = super().draw()
        return (dx + self.x + ((self.size + self.pad) * x),dy + self.y + ((self.size + self.pad) * y))
    def around_format(self):
        line1 = [block.Block(block.Block.barria) for _ in range(len(self.map[0]))]
        self.map[0] = line1
        for l in self.map:
            l[0] = block.Block(block.Block.barria)
            l[len(l) - 1] = block.Block(block.Block.barria)
        line2 = [block.Block(block.Block.barria) for _ in range(len(self.map[len(self.map) - 1]))]
        self.map[len(self.map) - 1] = line2
    def draw(self,screen:gui.Surface):
        font = pygame.font.Font(cash.font_path,self.size)
        for _t,t in enumerate(self.map):
            for _i,i in enumerate(t):
                loc = self.location(_i,_t)
                i.draw(screen.get_screen(),font,color.white,loc[0],loc[1])
    def setup(self,size):
        super().setup(size)
        self.around_format()

PAK.Package.MAP_HANDLER = NormalMap