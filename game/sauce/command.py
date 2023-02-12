from . import approach
from . import cash

def getDefaltSetting():
    return approach.CreateExTask(cash._server.get_socket(),approach.CODE_TYPES._GET_SETTING_DEFALT)