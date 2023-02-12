import socket
import element
import ai

from game.sauce.engine import block,map,enemy

class HandlerBase:
    def __init__(self,id:int) -> None:
        self.__socket:socket.socket = None
        self.__id = id
    @property
    def id(self):
        return self.__id
    @property
    def socket(self):
        return self.__socket
    @socket.setter
    def socket(self,value):
        if isinstance(value,socket.socket):
            self.__socket = value
    def dataSend(self,TYPE,value):
        element.dataSend(self.__socket,TYPE,value)
    def dataRecv(self):
        return element.dataRecv(self.__socket)

class BlockPackage(HandlerBase,block.Block):
    def __init__(self, id: int,blockID,cash) -> None:
        super(HandlerBase,self).__init__(id)
        super(block.Block,self).__init__(blockID,cash)
    @property
    def cash(self):
        return self.__cash
    def __reduce__(self):
        return (eval(Package._BLOCK_HANDLER),(self.id,self.cash))

class MapPackage(HandlerBase,map.NormalMap):
    def __init__(self,id,x,y,pad,MAP) -> None:
        super(HandlerBase,self).__init__(id)
        super(map.NormalMap,self).__init__(x,y,pad,MAP)
    def __reduce__(self):
        return (eval(Package._MAP_HANDLER),(self.x,self.y,self.pad,self.map))

class EnemyPackage(HandlerBase,enemy.Enemy):
    def __init__(self, id,MAP,mx,my):
        super(HandlerBase,self).__init__(id)
        super(enemy.Enemy,self).__init__(MAP,mx,my)
    def __reduce__(self):
        return (eval(Package._ENEMY_HANDLER),(self.map,self.mx,self.my))

class Package:
    _BLOCK_HANDLER = "Package.BLOCK_HANDLER"
    _MAP_HANDLER = "Package.MAP_HANDLER"
    _ENEMY_HANDLER = "Package.ENEMY_HANDLER"
    MAP_HANDLER = MapPackage
    BLOCK_HANDLER = BlockPackage
    ENEMY_HANDLER = EnemyPackage