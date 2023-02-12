from tkinter import messagebox
import tkinter as tk
import hashlib
import pickle
import socket
import os
from . import error
from . import approach
from .data import DATA
from . import setting
from .lang import LangWord
from .object.gaugebar import GuageBar
from .animation import easing

class FileScanGui(tk.Canvas):
    def __init__(self, master, root:tk.Tk, cnf: dict = {}, **opt) -> None:
        super().__init__(master, cnf, **opt)
        self.width = 100
        self.height = 100
        self.root = root
        self.namespace = self.__hash__()
    def update_size(self):
        self.update()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
    def show_title(self,title:LangWord):
        self.delete(f"{self.namespace}Title1")
        self.create_text(self.width / 2,self.height / 4,font=("Small Fonts",int(self.width / 25)),text=title.get(setting.language),tag=f"{self.namespace}Title1")
    def set_file_name(self,name):
        self.delete(f"{self.namespace}FileName1")
        self.create_text(self.width / 2,self.height / 2,text=name,font=("Bahnschrift SemiBold Condensed",int(self.width / 40)),tag=f"{self.namespace}FileName1")

class FileScan:
    def __init__(self,socket:socket.socket,server):
        self.socket = socket
        self.server = server
        self.__cmds = {
            1:{
                "detail":"FileScan開始の合図"
            }
        }
        self.guiHandler = None
        self.guageBar = None
    def set_bar(self,bar:GuageBar):
        self.guageBar = bar
    def set_gui(self,gui:FileScanGui):
        self.guiHandler = gui
    def response(self,data):
        if data.get_value()["id"] == 1:
            scan_files = approach.dataRecv(self.socket).get_value()
            hashs = self.get_files_hash(scan_files)
            self.server.stop()
            if self.guiHandler:
                self.guiHandler.root.after(1,self.SCAN,hashs)
            else:
                self.SCAN(hashs)
    def SCAN(self,datas:dict):
        logs = []
        if self.guageBar:
            self.guageBar.max_count(len(datas))
        for c,path in enumerate(datas):
            if self.guiHandler:
                self.guiHandler.set_file_name(path)
            if self.guageBar:
                self.guageBar.view(c)
            self.socket.send(DATA("respons",{"path":path,"hash":datas[path]}).encode())
            respons = approach.dataRecv(self.socket)
            logs.append(respons.get_value())
            print(respons.get_value())
        self.socket.send(DATA("finish",None).encode())
        result = approach.dataRecv(self.socket)
        self.server.restart()
        if result.get_value()["result"]:
            if self.guiHandler:
                self.guiHandler.root.after(300,lambda: self.guiHandler.show_title(LangWord(jp="C o n g l u t i n a t i o n !",en="C o m p l e t e !")))
                plot = easing.TotalInExpo(100,0,0.01,0,self.guiHandler.width + 15,1)
                self.guiHandler.root.after(700,lambda: easing.easing_canvas(self.guiHandler,plot,[0],100))
        else:
            messagebox.showerror(LangWord(jp="復元が必要です",en="Restoration is required.").get(setting.language),LangWord(jp="ファイルの整合性が確認できませんでした"))
    def get_files_hash(self,paths):
        hashs = {}
        for path in paths:
            HASH = ""
            if os.path.exists(path):
                print(path)
                with open(path,"r",encoding="UTF-8") as f:
                    HASH = hashlib.sha256(f.read().encode()).hexdigest()
            hashs.update({
                path:HASH
            })
        return hashs
    def start_scan(self):
        approach.dataSend(self.socket,DATA("FileScan",2).encode())
    def get_scan_files(self):
        request = DATA("FileScan",1)
        result = approach.dataComm(self.socket,request.encode())
        return result.get_value()