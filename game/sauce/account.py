import tkinter as tk
import socket
from venv import create

from .data import DATA
from . import approach
from .animation import easing
from . import error
from .lang import LangWord
from . import setting
from .text import TextH
from .form import EntryForm1,EntryForm1Sectors,scale_atach
from statistics import mean

approach._socket:socket.socket = None

class LOGIN_CANVAS(tk.Canvas):
    def __init__(self, master, cnf: dict = {}, **opt) -> None:
        super().__init__(master, cnf, **opt)
        self.width = 100
        self.height = 100
        self.words = {
            "main":[
                LangWord(jp="サインイン",en="Account Login"),
                LangWord(jp="ユーザー名",en="Account Name"),
                LangWord(jp="パスワード",en="password"),
                LangWord(jp="アカウントを作成",en="Create a new account"),
                LangWord(jp="ログイン",en="Login"),
                LangWord(jp="※ログイン後一定時間(10分)間はパスワードなしでログインできます",en="You can log in without password for a certain period of time (10 minutes) after logging in")
            ]
        }
    def size_update(self):
        self.update()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
    def login(self,after=lambda:None):
        result = login_account(self.username_entry.get(),self.password_entry.get())
        if result.get_value()[0]:
            after()
        else:
            log = approach.GetErrorLog(result.get_value()[1],lang=setting.language).get_value()[2]
            self.itemconfigure("title",text=log,fill="red")
    def setup(self,create_account=None,login=None):
        self.size_update()
        self.create_text(self.width / 2,self.height / 6,text=self.words["main"][0].get(setting.language),font=("",scale_atach(self,30)),tag="title")
        self.username_entry = tk.Entry(self,font=("",int(self.width / 55)))
        self.username_entry.place(x=self.width / 2,y=self.height / 3,anchor=tk.CENTER)
        self.create_text(self.width / 2,self.height / 3.5,text=self.words["main"][1].get(setting.language),font=("",scale_atach(self,50)))
        self.password_entry = tk.Entry(self,font=("",int(self.width / 55)))
        self.password_entry.place(x=self.width / 2,y=self.height / 2.2,anchor=tk.CENTER)
        self.create_text(self.width / 2,self.height / 2.5,text=self.words["main"][2].get(setting.language),font=("",scale_atach(self,50)))
        self.login_button = tk.Button(self,text=self.words["main"][4].get(setting.language),font=("",scale_atach(self,65)),fg="#7700ff",command=lambda: self.login(login))
        self.login_button.place(x=self.width / 2,y=self.height / 1.7,anchor=tk.CENTER)
        self.create_account_button = tk.Button(self,text=self.words["main"][3].get(setting.language),font=("",scale_atach(self,65)),fg="#7700ff",command=create_account)
        self.create_account_button.place(x=self.width / 2,y=self.height / 1.9,anchor=tk.CENTER)
        self.create_text(self.width / 2,self.height / 1.55,text=self.words["main"][5].get(setting.language),font=("",scale_atach(self,55)))

def create_account(name,pasword,nickname):
    result = approach.dataComm(DATA(approach.CODE_TYPES._CREATE_ACCOUNT,{"name":name,"password":pasword,"nickname":nickname}).encode(),approach.CODE_TYPES._RESULT)
    return result

def login_account(name,password):
    result = approach.dataComm(DATA(approach.CODE_TYPES._LOGIN,{"name":name,"password":password}).encode(),approach.CODE_TYPES._RESULT)
    return result

class AccountCreateCanvas(tk.Canvas):
    def __init__(self, master, cnf: dict = {}, **opt):
        super().__init__(master, cnf, **opt)
        self.__width = 100
        self.__height = 100
        self.__texts = TextH()
        self.__texts.add("title",LangWord(jp="Create a new account",en="Create a new account"))
        self.__texts.add("detail_pass",LangWord(jp="パスワード",en="Password"))
        self.__texts.add("detail_user",LangWord(jp="アカウントネーム",en="Account Name"))
        self.__texts.add("detail_nick",LangWord(jp="ニックネーム",en="Nick Name"))
        self.__texts.add("next",LangWord(jp="<< 次へ",en="<<< Next"))
        self.__texts.add("finish",LangWord(jp="< 完了 >",en="Done"))
        self.__texts.add("error1",LangWord(jp="<name>は<value>文字以上入力する必要があります",en="<name> must be at least <value> characters"))
        self.__detail_sectors = EntryForm1Sectors(self)
    def setup(self,after):
        self.size_update()
        self.__next_button = tk.Button(self,bg="white",text=self.__texts.get("next")[1].get(setting.language),font=("",scale_atach(self,40)),command=self.__detail_sectors.next)
        self.__next_button.place(relx=0.5,rely=0.75,anchor=tk.CENTER)
        self.__finish_button = tk.Button(self,bg="white",text=self.__texts.get("finish")[1].get(setting.language),font=("",scale_atach(self,40)),command=lambda: self.finish(after))
        self.__finish_button.place(relx=0.5,rely=0.85,anchor=tk.CENTER)
        password_form = EntryForm1(self,bg="sky blue",title=self.__texts.get("detail_pass")[1],border=4)
        userName_form = EntryForm1(self,bg="sky blue",title=self.__texts.get("detail_user")[1])
        nickName_form = EntryForm1(self,bg="sky blue",title=self.__texts.get("detail_nick")[1])
        self.__detail_sectors.add_sector(password_form)
        self.__detail_sectors.add_sector(userName_form)
        self.__detail_sectors.add_sector(nickName_form)
        self.__detail_sectors.draw(0,self.__width / 2,self.__height / 2)
    def finish(self,after_func):
        self.size_update()
        result = self.__detail_sectors.check()
        self.delete("log2")
        self.delete("log3")
        if result[0]:
            password_form_sct = self.__detail_sectors._get_sector(0)
            userName_form_sct = self.__detail_sectors._get_sector(1)
            nickname_form_sct = self.__detail_sectors._get_sector(2)
            result = create_account(self.__detail_sectors.get(userName_form_sct),self.__detail_sectors.get(password_form_sct),self.__detail_sectors.get(nickname_form_sct))
            print(self.__detail_sectors.get(userName_form_sct),self.__detail_sectors.get(password_form_sct),self.__detail_sectors.get(nickname_form_sct))
            if result.get_value()[0]:
                plot = easing.TotalInExpo(100,0,0.02,0,self.__width,1)
                easing.easing_canvas(self,plot,[0],10,command=lambda: [self.destroy,after_func])
            else:
                eor = approach.GetErrorLog(result.get_value()[1][0],setting.language).get_value()[2]
                self.create_text(self.__width / 2,self.__height / 4,text=eor,font=("",scale_atach(self,30)),fill="red",tag="log3")
        else:
            sector = result[1][0]
            value = self.__texts.get("error1")[1].get(setting.language).replace("<name>",str(sector.get_title())).replace("<value>",str(sector.get_border()))
            self.create_text(self.__width / 2,self.__height / 4,text=value,font=("",scale_atach(self,30)),tag="log2")
            index = self.__detail_sectors.get_index(sector)
            if index != None:
                self.__detail_sectors.SELECT(index)
            else:
                error.drop(6)
    def size_update(self):
        self.update()
        self.__width = self.winfo_width()
        self.__height = self.winfo_height()