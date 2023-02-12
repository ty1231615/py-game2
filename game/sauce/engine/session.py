import socket

from . import scene
from .. import approach,data

class SessionHandler:
    def __init__(self) -> None:
        self.__sessions = []
    @property
    def sessions(self):
        return self.__sessions
    def approach(self,data:data.DATA):
        rlt = False
        for ses in self.__sessions:
            if ses.id == data.get_type():
                print(f"Session approach: {data.get_type()}")
                ses.approach(data)
                rlt = True
        return rlt
    @property
    def ids(self):
        return [i.id for i in self.__sessions]
    def add(self,value):
        if isinstance(value,Session):
            self.__sessions.append(value)

class Session:
    _CMD_ID =           "SEI.APROACH.ID"
    _CMD =             "SEI.APROACH.CMD"
    _CMD_DATA =       "SEI.APROACH.DATA"
    def __init__(self,id,Scene:scene.Scene) -> None:
        self.__scene = Scene
        self.__id = id
    def approach(self,data:data.DATA):
        return True
    @property
    def id(self):
        return self.__id
    @property
    def Scene(self):
        return self.__scene
    @property
    def task(self):
        return self.__task
    def __del__(self):
        approach.dataSendDefalt(data.DATA(approach.CODE_TYPES._GAME_SESSION_DESTROY,{approach.CODE_TYPES._GAME_SESSION_ID:self.__id}))

class PracticeSession(Session):
    _CMD_GET_MAP =     "SEI.PRA.GET.MAP"
    _CMD_GET_ENEMY = "SEI.PRA.GET.ENEMY"
    _CMD_GET_PLAYER = "SEI.PRA.GET.PLAYER"
    _CMD_GET_ID =       "SEI.PRA.GET.ID"
    _CMD_POST_ENEMY = "SEI.PRA.POST.ENEMY"
    _CMD_POST_MAP = "SEI.PRA.POST.MAP"
    _CMD_GET_PROGRESS = "SEI.PRA.GET.PROG"
    def __init__(self, id, Scene: scene.Scene, socket:socket.socket) -> None:
        super().__init__(id, Scene)
        self.__socket = socket
        self.__map = self.Scene.cog.get("map")
        self.__player = self.Scene.cog.get("player")
        self.__enemy = self.Scene.cog.get("enemy")
        print(self.__player.package,self.__enemy.package)
    def approach(self, DATA: data.DATA):
        if DATA.get_value()[Session._CMD] == PracticeSession._CMD_GET_MAP:
            approach.dataSend(self.__socket,data.DATA(
                Session._CMD_DATA,self.__map.package
            ).encode())
        if DATA.get_value()[Session._CMD] == PracticeSession._CMD_GET_ENEMY:
            approach.dataSend(self.__socket,data.DATA(
                Session._CMD_DATA,self.__enemy.package
            ).encode())
        if DATA.get_value()[Session._CMD] == PracticeSession._CMD_GET_PLAYER:
            approach.dataSend(self.__socket,data.DATA(
                Session._CMD_DATA,self.__player.package
            ).encode())
        if DATA.get_value()[Session._CMD] == PracticeSession._CMD_GET_PROGRESS:
            approach.dataSend(self.__socket,data.DATA(
                Session._CMD_DATA,{
                    PracticeSession._CMD_GET_PLAYER:self.__player.package,
                    PracticeSession._CMD_GET_ENEMY:self.__enemy.package,
                    PracticeSession._CMD_GET_MAP:self.__map.package
                }
            ).encode())
        if DATA.get_value()[Session._CMD] == PracticeSession._CMD_POST_ENEMY:
            self.__enemy.package_update(*DATA.get_value()[Session._CMD_DATA])
    @property
    def Socket(self):
        return self.__socket
    @property
    def Map(self):
        return self.__map
    @property
    def Player(self):
        return self.__player
    @property
    def Enemy(self):
        return self.__enemy