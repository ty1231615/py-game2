import socket
import threading
import pickle
import os
import hashlib
import setting
import time
import math
import asyncio

import element
from error import ERROR
from ai import EnemyAI,NormalAI
import format

class FILE_REPAIR:
    def __init__(self,socket:socket.socket):
        self.__socket = socket
        self.__tasks = []
    @classmethod
    def get_file_data(cls,path,buffer,encode="UTF-8") -> tuple:
        datas = []
        if os.path.exists(path):
            with open(path,"r",encoding=encode) as f:
                data = ""
                for c,one in enumerate(f.read()):
                    data += one
                    if c % buffer == 0:
                        datas.append(data)
                        data = ""
        else:
            return (False,13)
        return (True,datas)
    def set_tasks(self,paths:dict):
        self.__tasks = paths
    def file_repair(self,path,buildPath,buffer,encode="UTF-8"):
        datas = FILE_REPAIR.get_file_data(path,buffer)
        if datas[0]:
            SD = element.DATA("FileRepair",{"controle":"new","encode":encode,"name":buildPath,"buffer":buffer})
            SD["buffer"] = len(SD.encode()) + 100
            self.__socket.send(SD.encode())
            progress = 0
            for data in datas[1]:
                self.__socket.send(element.DATA("FileRepair",{"progress":progress,"data":data}))
                result = element.dataRecv(self.__socket)
                progress += 1
        else:
            format.log.error(ERROR.get_detail(datas[1]))
    def repair(self):
        self.__socket.send(element.DATA("FileRepair","repair"))
        buffer = 1024
        for path in self.__tasks:
            self.file_repair(path,self.__tasks[path],buffer)
    def respons(self,data:element.DATA):
        if data.get_value() == 1:
            self.repair()

class FILE_SCAN:
    def __init__(self,socket:socket.socket):
        self.__socket = socket
        self.__tasks = []
        self.__scan_files = {}
        self.__scan_files_path = []
        self.__cmds = {
            1:{
                "detail":"確認が必要なファイルのパスを取得します",
                "name":"getFilesPath"
            }
        }
    def REQUEST(self):
        self.__tasks = self.__scan_files
        self.__socket.send(element.DATA("FileScan",{"id":1}).encode())
        print(self.__scan_files_path)
        self.__socket.send(element.DATA("PATHS",self.__scan_files_path).encode())
        while True:
            data = element.dataRecv(self.__socket)
            if data:
                print(data.get_type())
                if data.get_type() == "finish":
                    result = False
                    if not self.__tasks:
                        result = True
                    self.__socket.send(element.DATA(element.CODE_TYPES._RESULT,{element.CODE_TYPES._RESULT:result,"failure":[i for i in self.__tasks]}).encode())
                    break
                if data.get_type() == "respons":
                    if element.keyFact(data.get_value(),["path","hash"])[0]:
                        result = False
                        log = ""
                        RDATA = data.get_value()
                        #security
                        if RDATA["path"] in self.__tasks:
                            if RDATA["hash"] == self.__tasks[RDATA["path"]]:
                                #CLEAR
                                del self.__tasks[RDATA["path"]]
                                result = True
                                log = "success"
                            else:
                                log = "There is a difference in hash"
                        else:
                            log = "The path passed does not exist."
                    self.__socket.send(element.DATA(element.CODE_TYPES._RESULT,{element.CODE_TYPES._RESULT:result,"log":log}).encode())
            else:
                return
        print(f"[INFO] process finished 'FileScan' {self.__socket}")
    def response(self,data):
        if data.get_value() == 1:
            self.__socket.send(element.DATA("FileScan",self.__scan_files_path).encode())
        if data.get_value() == 2:
            self.REQUEST()
    def set_files_path(self,paths:list):
        self.__scan_files_path = paths
    def set_files(self,paths:dict):
        self.__scan_files = {}
        for path in paths:
            if os.path.exists(path):
                with open(path,"r",encoding="UTF-8") as f:
                    hash = hashlib.sha256(f.read().encode()).hexdigest()
                    self.__scan_files.update(
                        {
                            paths[path]:hash
                        }
                    )
            else:
                print(f"[ERROR] `{path}`というパスのファイルは存在しません")
    def get_files(self):
        return self.__scan_files
    def scan(self,path,hash):
        if path in self.__scan_files:
            if self.__scan_files[path] == hash:
                return (True,path)
            else:
                return (False,"ハッシュ値が異なっています",path)
        else:
            return (False,f"`{path}`というファイルのハッシュは必要ではありません",path)

class TaskHander:
    def __init__(self) -> None:
        self.__tasks = []
    def add(self,task):
        if isinstance(task,Task):
            self.__tasks.append(task)
    def get_tasks(self):
        return self.__tasks
    def complete(self,task,value):
        rlt = False
        for tsk in self.get_tasks():
            if tsk.task == task:
                tsk.complete(value)
                rlt = True
        return rlt

class Task:
    def __init__(self,task) -> None:
        self.__task = task
        self.__cmp = False
        self.__data = None
    def complete(self,value:element.DATA):
        self.__data = value
        self.__cmp = True
    def _(self):
        while True:
            if self.__cmp:
                return self.__data
    @property
    def task(self):
        return self.__task

class ExTaskRecv:
    def __init__(self,task) -> None:
        self.__task = task
        self.__datas = []
        self.__data = None
        self.__progress = 0
        self.__finish = False
    def get_task(self):
        return self.__task
    def pickleDatas(self):
        datas = ""
        for d in self.__datas:
            datas += d
        return pickle.loads(datas)
    def finish(self,data):
        self.__finish = True
        self.__data = data
    def controle(self,recv:element.DATA):
        if recv.get_value()[0] == element.CODE_TYPES._EXACT_TASK_FINISH:
            data = self.pickleDatas()
            self.finish()
        else:
            self.__finish = True
    def progress(self,recv:element.DATA):
        if recv.get_value()[0] == element.CODE_TYPES._EXACT_TASK_SEND:
            self.__datas.append(recv.get_value()[1])
            self.__progress += 1
        else:
            self.controle(recv)
    def wait(self):
        while True:
            if self.__finish:
                return self.__data

class ExTaskSender:
    def __init__(self,socket:socket.socket,data,accessId) -> None:
        self.__data = pickle.dumps(data)
        self.__socket = socket
        self.__send_id = accessId
    def _SLASH_DATA(self,scale):
        new = []
        for i in range(math.ceil(len(self.__data) / scale)):
            new.append(self.__data[i * scale:(i+1) * scale])
        return new
    def start(self,buffer=1024):
        print(f"START EX TASK {self.__send_id}")
        if self.__status:
            datas = self._SLASH_DATA(buffer)
            print(datas)
            for i,data in enumerate(datas):
                print(data)
                element.dataRecv(self.__socket)
                self.__sending(data)
                element.dataRecv(self.__socket)
                print(f"[ExTask] Complete sended progress:{i}")
            element.dataRecv(self.__socket)
            self.__complete()
            print("[ExTask] Finish sended")
    def controle(self,data:element.DATA) -> bool:
        if data.get_type() == element.CODE_TYPES._EXACT_TASK_STATUS:
            if element.keyFact(data.get_value(),["StandBy"]):
                if data.get_value()["StandBy"]:
                    return (True,)
        if data.get_type() == element.CODE_TYPES._EXACT_TASK_CONTINUE:
            if data.get_value():
                return (True,)
        if data.get_type() == element.CODE_TYPES._EXACT_EX_FAILURE:
            return (False,7)
        return (False,0)
    def _start(self):
        element.dataSend(self.__socket,element.CODE_TYPES._EXACT_TASK_CNT,{
            element.CODE_TYPES._EXACT_TASK_NAME:self.__send_id,
        })
        rlt = element.dataRecv(self.__socket)
        if rlt.get_type() == element.CODE_TYPES._EXACT_TASK_CNT:
            return True
        else:
            return False
    def __status(self) -> bool:
        recv = element.dataRecv(self.__socket)
        result = self.controle(recv)
        if result[0]:
            return True
        else:
            ERROR.get_detail(result[1])
            return False
    def __sending(self,data) -> bool:
        element.dataSend(self.__socket,self.__send_id,{
            element.CODE_TYPES._EXACT_COMMAND:element.CODE_TYPES._EXACT_TASK_SEND,
            element.CODE_TYPES._EXACT_TASK_NAME:self.__send_id,
            element.CODE_TYPES._EXACT_TASK_SENDING:data,
        })
    def __complete(self):
        element.dataSend(self.__socket,self.__send_id,{
            element.CODE_TYPES._EXACT_COMMAND:element.CODE_TYPES._EXACT_TASK_FINISH
        })

class ExTaskRecvHandler:
    def __init__(self) -> None:
        self.__tasks = []
    def get(self,index):
        return self.__tasks[index]
    def gets(self):
        return self.__tasks
    def add(self,task):
        if isinstance(task,ExTaskRecv):
            self.__tasks.append(task)
    def attach(self,task,recv:element.DATA):
        for i in self.gets():
            if i.get_task() == task:
                i.progress(recv)

class SERVER:
    def __init__(self) -> None:
        self.__started = False
        self.CLIENT_HANDLERS = []
        self.__socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def start(self):
        if not self.__started:
            self.__started = True
            self.__socket.bind(("0.0.0.0",55412))
            self.__socket.listen(20)
            print("Starting data server")
            while True:
                clientsocket,address = self.__socket.accept()
                print(f"[access] port:{address[1]} | ip:{address[0]} が接続しました")
                clientHandler = CustomerControler(address[1],address[0],clientsocket)
                self.CLIENT_HANDLERS.append(clientHandler)
        else:
            return (False,"[ERROR] The data server is already up and running.")

def create_user(name,password,nickname=None):
    if element.UserData.name_check(name):
        user = element.UserData(name)
        if nickname:
            user.set_nickname(nickname)
        user.get_login().set_password(password)
        user.get_login().login(password)
        user.save()
        return user
    else:
        return ERROR.get_detail(3)

def _task(handler:TaskHander,task:Task):
    handler.add(task)
    return task._()

class CustomerControler:
    def __init__(self,port,ip,socket:socket.socket=None) -> None:
        self.__ip = ip
        self.__port = port
        self.__working = False
        self.__socket = socket
        self.__sessions = SessionHandler()
        self.task_handler = TaskHander()
        self.FILE_SCAN = FILE_SCAN(self.__socket)
        self.FILE_SCAN.set_files(setting.scan_files)
        self.FILE_SCAN.set_files_path([setting.scan_files[i] for i in setting.scan_files])
        self.FILE_REPAIR = FILE_REPAIR(self.__socket)
        self.FILE_REPAIR.set_tasks(setting.scan_files)
        self.__EX_TASKRE_HANDLER = ExTaskRecvHandler()
        self.__account = None
        if self.__socket:
            threading.Thread(target=self._).start()
    @property
    def working(self):
        return self.__working
    def account_save(self):
        if self.__account:
            print(f"saved: {self.__account.get_name()} | {self.__ip} | {self.__account}")
            self.__account.get_login().logout()
            self.__account.save()
        else:
            print(f"[NotLoginAccount] {self.__ip}")
    def dataSend(self,type,value):
        element.dataSend(self.__socket,type,value)
    def dataRecv(self):
        return element.dataRecv(self.__socket)
    def _(self):
        self.__working = True
        while True:
            try:
                recv = pickle.loads(self.__socket.recv(8192))
            except Exception as e:
                print(e)
                self.account_save()
                self.__sessions.destroy()
                self.__working = False
                return
            if element.keyFact(recv,["type","value"])[0]:
                recv = element.DATA.ENCODE(recv)
                print(f"[log] recive data by {self.__ip}")
                #GAME ACT
                if self.task_handler.complete(recv.get_type(),recv):
                    continue
                if recv.get_type() == element.CODE_TYPES._GAME_SESSION_BIND:
                    session = Session(self,recv.get_value().get("type"))
                    self.__sessions.add(session)
                    self.dataSend(element.CODE_TYPES._GAME_SESSION_BIND,{element.CODE_TYPES._GAME_SESSION_ID:session.id})
                    continue
                elif recv.get_type() == element.CODE_TYPES._GAME_SESSION_START:
                    session = self.__sessions.get(recv.get_value())
                    if session:
                        threading.Thread(target=session.load).start()
                    else:
                        self.dataSend("raise",0)
                    continue
                elif recv.get_type() == element.CODE_TYPES._GAME_SESSION_DESTROY:
                    id = recv.get_value().get(element.CODE_TYPES._GAME_SESSION_ID)
                    self.__sessions.remove(id)
                    continue
                #exit code
                if recv.get_type() == element.CODE_TYPES._EXIT:
                    print(f"[log] Exit Server Approach {self.__ip}")
                    self.dataSend(element.CODE_TYPES._EXIT,True)
                    self.account_save()
                    self.__sessions.destroy()
                    return
                if recv.get_type() == "test":
                    self.__socket.send(pickle.dumps(element.DATA("message","hey see you")))
                elif recv.get_type() == element.CODE_TYPES._FILE_SCAN:
                    self.FILE_SCAN.response(recv)
                elif recv.get_type() == element.CODE_TYPES._FILE_REPAIR:
                    self.FILE_REPAIR.respons(recv)
                elif recv.get_type() == element.CODE_TYPES._CREATE_ACCOUNT:
                    try:
                        name = recv.get_value()["name"]
                        password = recv.get_value()["password"]
                        nickname = recv.get_value()["nickname"]
                    except:
                        self.dataSend(element.CODE_TYPES._RESULT,(False,2))
                    account = create_user(name,password,nickname)
                    if isinstance(account,element.UserData):
                        self.dataSend(element.CODE_TYPES._RESULT,(True,))
                    else:
                        self.dataSend(element.CODE_TYPES._RESULT,(False,account))
                    continue
                elif recv.get_type() == element.CODE_TYPES._GET_ERROR:
                    index = int(recv.get_value().get("index",0))
                    lang = recv.get_value().get("lang","en")
                    error = ERROR.get_detail(index,lang=lang)
                    self.dataSend(element.CODE_TYPES._RESULT,error)
                    continue
                elif recv.get_type() == element.CODE_TYPES._LOGIN:
                    name = recv.get_value().get("name")
                    password = recv.get_value().get("password")
                    lang = recv.get_value().get("lang","en")
                    account:element.UserData = element.UserData.get_instance_by_name(name)
                    if account:
                        login_pointer = account.get_login()
                        if login_pointer.logined():
                            self.__account = account
                            self.dataSend(element.CODE_TYPES._RESULT,(True,))
                        else:
                            if login_pointer.login(password):
                                self.__account = account
                                self.dataSend(element.CODE_TYPES._RESULT,(True,))
                            else:
                                self.dataSend(element.CODE_TYPES._RESULT,(False,4))
                    else:
                        self.dataSend(element.CODE_TYPES._RESULT,(False,5))
                elif recv.get_type() == element.CODE_TYPES._CREATE_EX_GET:
                    if element.keyFact(recv.get_value(),[element.CODE_TYPES._EXACT_TASK_ID,element.CODE_TYPES._EXACT_COMMAND]):
                        cmd = recv.get_value()[element.CODE_TYPES._EXACT_COMMAND]
                        if cmd == element.CODE_TYPES._GET_SETTING_DEFALT:
                            sender = ExTaskSender(self.__socket,setting.game_defalt_setting,recv.get_value()[element.CODE_TYPES._EXACT_TASK_ID])
                            if sender._start():
                                sender.start()
                            continue
                        else:
                            print(f"[error] No found ExTask: {recv.get_value()[element.CODE_TYPES._EXACT_TASK_ID]}")
                            self.dataSend(element.CODE_TYPES._EXACT_EX_FAILURE,recv.get_value()[element.CODE_TYPES._EXACT_TASK_ID])
                    else:
                        self.dataSend(element.CODE_TYPES._EXACT_EX_FAILURE,8)
                elif self.__account:
                    pass
                else:
                    self.dataSend("raise",0)
            else:
                print("[ERROR] We don't have all the data we need.")
                continue

class SessionHandler:
    def __init__(self) -> None:
        self.__sessions = []
    @property
    def sessions(self):
        return self.__sessions
    def destroy(self):
        for ses in list(self.__sessions):
            ses.stop()
    def get(self,id):
        for ses in self.__sessions:
            if isinstance(ses,Session):
                if ses.id == id:
                    return ses
    def remove(self,id):
        for session in self.__sessions:
            if session.id == id:
                self.__sessions.remove(session)
                del session
    def add(self,value):
        if isinstance(value,Session):
            self.__sessions.append(value)

class Session:
    _CMD =             "SEI.APROACH.CMD"
    _CMD_ID =           "SEI.APROACH.ID"
    _CMD_DATA =       "SEI.APROACH.DATA"
    _CMD_GET_MAP =     "SEI.PRA.GET.MAP"
    _CMD_GET_ENEMY = "SEI.PRA.GET.ENEMY"
    _CMD_GET_PLAYER="SEI.PRA.GET.PLAYER"
    _CMD_GET_ID =       "SEI.PRA.GET.ID"
    _CMD_POST_ENEMY = "SEI.PRA.POST.ENEMY"
    _CMD_GET_PROGRESS = "SEI.PRA.GET.PROG"
    def __init__(self,client:CustomerControler,sessionTYPE) -> None:
        self.__client = client
        self.__id = self.__hash__()
        self.__update_flame = 0.5
        self.__asy_loop = asyncio.new_event_loop()
        self.__map = []
        self.__players = []
        self.__enemys = []
        self.__enemy_ai = None
        self.__RNG = False
        self.__session_type = sessionTYPE
    def dataSend(self,TYPE,value):
        self.__client.dataSend(
            self.__id,
            {
                Session._CMD:TYPE,
                Session._CMD_DATA:value
            }
        )
    def respons(self,code,data,task_name):
        self.dataSend(code,data)
        return self.create_task(task_name)
    def create_task(self,task_name:str):
        return _task(self.__client.task_handler,Task(task_name))
    def dataRecv(self):
        return self.__client.dataRecv()
    def load(self):
        if self.__session_type == element.CODE_TYPES._GAME_SESSION_TYPE_PRACTICE:
            print(f"load practice session [{self.__id}]")
            self.__asy_loop.run_until_complete(self.load_practice())
        else:
            print(f"No match type of session {self}")
            return False
    def stop(self):
        self.__RNG = False
    async def load_practice(self):
        map_data = self.respons(Session._CMD_GET_MAP,None,Session._CMD_DATA).get_value()
        self.__map.append(map_data)
        enemy_data = self.respons(Session._CMD_GET_ENEMY,None,Session._CMD_DATA).get_value()
        self.__enemys.append(enemy_data)
        self.__enemy_ai = EnemyAI.ioad_ai(enemy_data[3])(enemy_data[0],enemy_data[1])
        player_data = self.respons(Session._CMD_GET_PLAYER,None,Session._CMD_DATA).get_value()
        self.__players.append(player_data)
        self.__RNG = True
        await self.enemy_task()
    async def enemy_task(self):
        if self.__RNG:
            progress = self.respons(Session._CMD_GET_PROGRESS,None,Session._CMD_DATA).get_value()
            enemy = progress.get(Session._CMD_GET_ENEMY)
            MAP = progress.get(Session._CMD_GET_MAP)
            player_data = progress.get(Session._CMD_GET_PLAYER)
            x,y = self.__enemy_ai.get_optimal((enemy[0],enemy[1]),(player_data[0],player_data[1]))
            self.__enemys[0] = (x,y,*enemy[2:])
            self.dataSend(Session._CMD_POST_ENEMY,(x,y,enemy[2]))
            print(f"[{self.__id} progress] move enemy")
            await asyncio.sleep(self.__update_flame)
            await self.enemy_task()
    def start(self):
        self.client.dataSend(
            element.CODE_TYPES._GAME_SESSION_BIND,
            {element.CODE_TYPES._GAME_SESSION_ID:self.__id}
        )
        self.load(self.__session_type)
    @property
    def enemys(self):
        return self.__enemys
    @property
    def players(self):
        return self.__players
    @property
    def map(self):
        return self.__map
    @property
    def client(self):
        return self.__client
    @property
    def id(self):
        return self.__id