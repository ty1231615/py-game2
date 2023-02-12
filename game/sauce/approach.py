import socket
import pickle
import time
import math
import traceback
import tkinter as tk
import threading

from . import data as dataC
from . import error
from . import setting
from . import security
from . import cash
from .PAK import Package

from .engine.session import Session,SessionHandler

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


def dataRecv(sck:socket.socket) -> dataC.DATA:
    data = pickle.loads(sck.recv(8192))
    if dataC.keyFact(data,["type","value"])[0]:
        data = dataC.DATA(data["type"],data["value"])
        return data
    else:
        error.drop(4,lang=setting.language)

def dataSend(socket:socket.socket,data):
    try:
        socket.send(data)
    except Exception as e:
        cls = e.__class__
        log = traceback.format_exc()
        cash._root.after(0,lambda: error.EOR(cls,log))

def dataSendDefalt(data):
    try:
        _socket.send(data)
        return True
    except Exception as e:
        cls = e.__class__
        log = traceback.format_exc()
        cash._root.after(0,lambda: error.EOR(cls,log))

def dataComm(data,taskName):
    send = dataSendDefalt(data)
    if send:
        return CreateTask(taskName)

class Task:
    _TASKS = []
    def __init__(self,type) -> None:
        self.__type = type
        self.__complete = False
        self.__data = None
        Task._TASKS.append(self)
    @property
    def data(self):
        return self.__data
    @property
    def cpt(self):
        return self.__complete
    def _(self):
        while True:
            if self.__complete:
                return self.__data
    def get_task(self):
        return self.__type
    def remove(self):
        Task._TASKS.remove(self)
        del self
    def complete(self,data:dataC.DATA):
        self.__complete = True
        self.__data = data

class ExactTaskRecv:
    _TASKS = []
    @classmethod
    def cancel(cls,task):
        if isinstance(task,ExactTaskRecv):
            task.cancel()
    @classmethod
    def start(cls,_socket:socket.socket,task):
        if isinstance(task,ExactTaskRecv):
            dataSend(_socket,dataC.DATA(CODE_TYPES._EXACT_TASK_CNT,None).encode())
            task._start()
            return
        dataSend(_socket,dataC.DATA(CODE_TYPES._EXACT_EX_FAILURE,None).encode())
    @classmethod
    def get(cls,name):
        for i in ExactTaskRecv._TASKS:
            if i.get_id() == name:
                if isinstance(i,ExactTaskRecv):
                    return i
    def __init__(self,socket:socket.socket,command) -> None:
        ExactTaskRecv._TASKS.append(self)
        self.__socket = socket
        self.__id = str(self.__hash__())
        self.__stand_by = False
        self.__finish = False
        self.__cancel = False
        self.__cmd = command
        self.__cash = []
        dataSend(self.__socket,dataC.DATA(CODE_TYPES._CREATE_EX_GET,{
            CODE_TYPES._EXACT_TASK_ID:self.__id,
            CODE_TYPES._EXACT_COMMAND:self.__cmd
        }).encode())
    def get_status(self):
        return {
            "StandBy":self.__stand_by
        }
    def _start(self):
        self.__stand_by = True
        dataSend(self.__socket,dataC.DATA(CODE_TYPES._EXACT_TASK_STATUS,self.get_status()).encode())
        while True:
            dataSend(self.__socket,dataC.DATA(CODE_TYPES._EXACT_TASK_WAIT,None).encode())
            result = dataRecv(self.__socket)
            print(result.get_value()[CODE_TYPES._EXACT_COMMAND])
            if result.get_value()[CODE_TYPES._EXACT_COMMAND] == CODE_TYPES._EXACT_TASK_SEND:
                self.__cash.append(
                    result.get_value()[CODE_TYPES._EXACT_TASK_SENDING]
                )
                dataSend(self.__socket,dataC.DATA(CODE_TYPES._EXACT_TASK_WAIT,None).encode())
                continue
            elif result.get_value()[CODE_TYPES._EXACT_COMMAND] == CODE_TYPES._EXACT_TASK_FINISH:
                break
        print("FINISH")
        self.finish()
    def FORMAT(self):
        data = bytes()
        for cash in self.__cash:
            data += cash
        print(data)
        return pickle.loads(data)
    def cancel(self):
        self.__cancel = True
    def finish(self):
        self.__finish = True
    def Complete(self):
        while True:
            if self.__finish:
                return self.FORMAT()
            if self.__cancel:
                del self
                return
    def get_id(self):
        return self.__id

def CreateExTask(socket,cmd):
    reciver = ExactTaskRecv(socket,cmd)
    result = reciver.Complete()
    del reciver
    return result

class ExactTaskSend:
    def __init__(self,task,data:dataC.DATA) -> None:
        self.__task = task
        self.__data = data.encode()
        self.__started = False
        self.__id = str(self.__hash__())
    def SLASH_DATA(self,scale):
        new = []
        for i in range(math.ceil(len(self.__data) / scale)):
            new.append(self.__data[i * scale:(i+1) * scale])
        return new
    def __SEND(self):
        sendData = self.SLASH_DATA(1024)
        for data in sendData:
            dataSendDefalt(dataC.DATA(self.__task,(CODE_TYPES._EXACT_TASK_SEND,data)))
        return self.__FINISH()
    def __FINISH(self):
        dataSendDefalt(dataC.DATA(self.__task,(CODE_TYPES._EXACT_TASK_FINISH,"Finish Approach")))
        result = CreateTask(self.__task)
        return result
    def start(self):
        if not self.__started:
            self.__started = True
            dataSendDefalt(dataC.DATA(CODE_TYPES._EXACT_TASK,(self.__task,CODE_TYPES._SEND,self.__id)))
            result = CreateTask(self.__id)
            if result.get_value()[0]:
                return self.__SEND()
            else:
                return False
 
class DataServerHandler:
    def __init__(self):
        self.__connected = False
        self.__socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__stop = False
        self.__sessions = SessionHandler()
    @property
    def socket(self):
        return self.__socket
    @property
    def sessions(self):
        return self.__sessions
    @property
    def is_stop(self):
        return self.__stop
    @property
    def is_connect(self):
        return self.__connected
    def set_fileScan(self,file_scan:security.FileScan):
        self.file_scan = file_scan
    def get_socket(self):
        return self.__socket
    def disconnect(self):
        dataSendDefalt(dataC.DATA(CODE_TYPES._EXIT,True).encode())
        while not self.__connected:
            print("Server Disconnect")
            return
    def connect(self,ads):
        if not self.__connected:
            try:
                self.__socket.connect((ads,55412))
            except ConnectionRefusedError:
                return (False,1,"サーバーに接続できませんでした")
            self.__connected = True
        else:
            return (False,2,"既にサーバーに接続されています")
        return (True,)
    def stop(self):
        self.__stop = True
    def restart(self):
        self.__stop = False
    def _receive(self,eor):
        while True:
            if self.__stop:
                time.sleep(0.01)
                continue
            try:
                data = dataRecv(self.__socket)
            except Exception as e:
                self.__connected = False
                log = e.__class__
                logs = traceback.format_exc()
                cash._root.after(0,lambda: eor(log,logs))
                return
            if not data:
                continue
            if self.__sessions.approach(data):
                continue
            ctn = False
            #Task Handle
            for task in list(Task._TASKS):
                type = task.get_task()
                if type == data.get_type():
                    task.complete(data)
                    task.remove()
                    ctn = True
                    break
            if ctn:
                continue
            if data.get_type() == "FileScan":
                if self.file_scan:
                    self.file_scan.response(data)
                continue
            if data.get_type() == "FileRepair":
                if self.file_repair:
                    self.file_repair.response(data)
                continue
            if data.get_type() == CODE_TYPES._EXIT:
                self.__connected = False
                print("Server approach is closed")
                self.__socket.close()
                return
            if data.get_type() == CODE_TYPES._EXACT_EX_FAILURE:
                ExTask = ExactTaskRecv.get(data.get_value())
                ExactTaskRecv.cancel(ExTask)
                continue
            if data.get_type() == CODE_TYPES._EXACT_TASK_CNT:
                print(data.get_value()[CODE_TYPES._EXACT_TASK_NAME])
                ExTask = ExactTaskRecv.get(data.get_value()[CODE_TYPES._EXACT_TASK_NAME])
                ExactTaskRecv.start(self.__socket,ExTask)
                continue
_server:DataServerHandler = None
_socket:socket.socket = None

class Account:
    def __init__(self) -> None:
        pass

def CreateTask(type):
    task = Task(type)
    return task._()

def GetErrorLog(index,lang=setting.language):
    result = dataComm(dataC.DATA("GetError",{"index":index,"lang":lang}).encode(),CODE_TYPES._RESULT)
    return result