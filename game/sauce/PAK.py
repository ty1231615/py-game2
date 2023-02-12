import pickle

class Package:
    _ENEMY_HANDLER = "Package.ENEMY_HANDLER"
    _MAP_HANDLER = "Package.MAP_HANDLER"
    _BLOCK_HANDLER = "Package.BLOCK_HANDLER"
    ENEMY_HANDLER = None
    MAP_HANDLER = None
    BLOCK_HANDLER = None
    __PACKS = []
    def __init__(self) -> None:
        self.__id = self.__hash__()
        Package.__PACKS.append(self)
    def __del__(self):
        if self in Package.__PACKS:
            Package.__PACKS.remove(self)
    @classmethod
    def GET_PACKS(self):
        return Package.__PACKS
    @property
    def package_id(self):
        return self.__id