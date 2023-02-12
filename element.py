import datetime
import socket
import os
import pickle
import hashlib

class CODE_TYPES:
    _RESULT =                      "result"
    _EXIT =                       "000EXIT"
    _FILE_SCAN =                 "FileScan"
    _FILE_REPAIR =             "FileRepair"
    _CREATE_ACCOUNT =       "CreateAccount"
    _LOGIN_ACCOUNT =         "LoginAccount"
    _GET_ERROR =                 "GetError"
    _LOGIN =                        "login"
    _EXACT_TASK =                  "ExTask"
    _EXACT_TASK_SENDING =       "ExSending"
    _EXACT_TASK_CNT =       "ExTaskContact"
    _EXACT_TASK_WAIT =         "ExTaskWait"
    _EXACT_TASK_STATUS =     "ExTaskStatus"
    _EXACT_TASK_SEND =             "ExPost"
    _EXACT_TASK_NAME =         "ExTaskName"
    _EXACT_TASK_RECV =              "ExGet"
    _CREATE_EX_GET =             "ReiExGet"
    _CREATE_EX_SEND =           "ReiExSend"
    _EXACT_EX_FAILURE =     "ExTaskFailure"
    _EXACT_TASK_CONTINUE = "ExTaskContinue"
    _EXACT_TASK_RESULT =     "ExTaskResult"
    _EXACT_TASK_FINISH =         "ExFinish"
    _EXACT_TASK_ID =             "ExTaskID"
    _EXACT_COMMAND =            "ExCommand"
    _RECV =                           "GET"
    _SEND =                          "SEND"
    #exact commands
    _GET_SETTING_DEFALT ="GetSettingDefalt"
    #developer tool
    _DEV_LOGIN = "DEV_LOGIN"
    #GAME
    _GAME_ENEMY_BIND =         "P.ENE.BIND"
    _GAME_ENEMY_ID =             "P.ENE.ID"
    _GAME_ENEMY_MOVE =         "P.ENE.MOVE"
    _GAME_ENEMY_DESTROY =   "P.ENE.DESTROY"
    _GAME_SESSION_POST =        "P.SEI.PST"
    _GAME_SESSION_BIND =       "P.SEI.BIND"
    _GAME_SESSION_DESTROY = "P.SEI.DESTROY"
    _GAME_SESSION_ID =           "P.SEI.ID"
    _GAME_SESSION_START =     "P.SEI.START"
    _GAME_SESSION_TYPE_PRACTICE = "P.SEI.TYPE.P"


class DATA:
    def __init__(self,type,value) -> None:
        self.__type = type
        self.__value = value
    def get_type(self):
        return self.__type
    def get_value(self):
        return self.__value
    def encode(self):
        return pickle.dumps(self)
    def __reduce__(self):
        return (dict,({"type":self.__type,"value":self.__value},))
    @classmethod
    def ENCODE(cls,data:dict):
        instance = DATA(data["type"],data["value"])
        return instance

class LoginPointer:
    permission_second = 500
    def __init__(self) -> None:
        self.__last_login = None
        self.__password = None
        self.__login = False
    def login(self,password):
        if password == self.__password:
            self.__last_login = datetime.datetime.now()
            self.__login = True
            return True
        return False
    def logined(self):
        if not self.__last_login:
            return False
        time = datetime.datetime.now() - self.__last_login
        if time.total_seconds() > LoginPointer.permission_second:
            return False
        else:
            return True
    def get_login(self):
        return self.__login
    def logout(self):
        self.__login = False
    def set_password(self,value):
        self.__password = value

users_folder_path = "users"
dev_account_path = "devs"

class UserData:
    _INSTACE = []
    def __init__(self,name) -> None:
        self.__name = name
        self.__nickname = name
        self.__password = None
        self.__login = LoginPointer()
        self.__id = hashlib.sha224(str(self.__name).encode()).hexdigest()
        UserData.__add_instance(self)
    @classmethod
    def LOADS(cls):
        files = os.listdir(users_folder_path)
        for path in files:
            instance = pickle.loads(open(f"{users_folder_path}/{path}","br").read())
            UserData.__add_instance(instance)
            print(instance.get_name())
    @classmethod
    def __add_instance(cls,instance):
        if isinstance(instance,UserData):
            UserData._INSTACE.append(instance)
    @classmethod
    def name_check(cls,value:str):
        if value in [i.get_name() for i in UserData._INSTACE]:
            return False
        return True
    @classmethod
    def get_instance_by_name(cls,name):
        for user in UserData._INSTACE:
            if name == user.get_name():
                return user
    def set_name(self,new):
        self.__name = new
    def get_name(self):
        return self.__name
    def set_nickname(self,new):
        self.__nickname = new
    def get_nickname(self):
        return self.__nickname
    def get_login(self):
        return self.__login
    def save(self):
        pickle.dump(self,open(f"{users_folder_path}/{self.__id}","wb"))
    def set_password(self,password,before=None):
        if self.__password:
            if before == password:
                self.__password = password
                self.__login.set_password(password)
                return True
            return False
        else:
            self.__password = password
            return True
    def get_password(self,password):
        if password == self.__password:
            return self.__password

#developer Account
class DeveloperUser(UserData):
    def login(self):
        pass

def dataRecv(socket:socket.socket) -> DATA:
    data = pickle.loads(socket.recv(8192))
    if keyFact(data,["type","value"])[0]:
        data = DATA(data["type"],data["value"])
        return data
    else:
        print(f"[ERROR] 受け取ったデータに整合性がありません | {data}")

def dataSend(socket:socket.socket,type,value): 
    socket.send(pickle.dumps(DATA(type,value)))

def keyFact(obj:dict,keys:list):
    if all(i in obj for i in keys):
        return (True,)
    else:
        return (False,[i in obj for i in keys],[i not in obj for i in keys])

def valueFact(*arg):
    return all([bool(i) for i in arg])

def attrFact(obj,attrs:list):
    if all(i in obj.__dict__ for i in attrs):
        return (True,)
    else:
        return (False,[i for i in attrs if i in obj.__dict__],[i for i in attrs if not i in obj.__dict__])