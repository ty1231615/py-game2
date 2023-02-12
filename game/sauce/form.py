import tkinter as tk
from unittest import result

from .animation import easing
from .lang import LangWord
from .text import TextH
from . import setting
from statistics import mean

def scale_atach(cvs:tk.Canvas,slash:int):
    cvs.update()
    return int(mean([cvs.winfo_width(),cvs.winfo_height()]) / slash)

class Sector(tk.Canvas):
    def __init__(self,master, cnf: dict = {}, **opt):
        super().__init__(master, cnf, **opt)
        self.__width = 100
        self.__height = 100
        self._setup = False
        self.__input = False
    def inputed(self):
        self.__input = True
    def get_inputed(self):
        return self.__input
    def get_data(self):
        return None
    def get_width(self):
        return self.__width
    def get_height(self):
        return self.__height
    def supdate(self):
        self.update()
        self.__width = self.winfo_width()
        self.__height = self.winfo_height()

class EntryForm1(Sector):
    def __init__(self,master, cnf: dict = {},title="No title",border=1, **opt):
        super().__init__(master, cnf, **opt)
        self.__text = TextH()
        self.__text.add("title",title)
        self.__border = border
        self.__entry = tk.Entry(self,font=("",20))
    def get_border(self):
        return self.__border
    def get_title(self):
        return self.__text.get("title")[1].get(setting.language)
    def result(self):
        return self.__entry.get()
    def check(self):
        if self.__border <= len(self.result()):
            return True
        return False
    def setup(self):
        self.supdate()
        if not self._setup:
            self._setup = True
            title = self.__text.get("title")
            self.create_text(self.get_width() / 2,self.get_height() / 4.5,text=title[1].get(setting.language),tag=title[0],font=("",int(mean([self.get_width(),self.get_height()]) / 12)))
            self.__entry.place(x=self.get_width() / 2,y=self.get_height() / 2,anchor=tk.CENTER)
            self.__entry["font"] = ("",scale_atach(self,15))


class EntryForm1Sectors:
    def __init__(self,canvas:tk.Canvas) -> None:
        self.__SECTORS = []
        self.__select = 0
        self.__cvs = canvas
        self.__center_x = 0
        self.__center_y = 0
        self.__width = 0
        self.__height = 0
        self._before = 0
    def check(self):
        c = []
        nc = []
        for i in self.__SECTORS:
            if isinstance(i,EntryForm1):
                if i.check():
                    c.append(i)
                else:
                    nc.append(i)
        if nc:
            return (False,nc)
        else:
            return (True,c)
    def get(self,instance:EntryForm1):
        if instance in self.__SECTORS:
            print(instance.result())
            return instance.result()
    def update_cvs(self):
        self.__cvs.update()
        self.__center_x = self.__cvs.winfo_width() / 2
        self.__center_y = self.__cvs.winfo_height() / 2
        self.__width = self.__cvs.winfo_width()
        self.__height = self.__cvs.winfo_height()
    def _get_sector(self,index):
        instance = self.__SECTORS[index]
        if isinstance(instance,EntryForm1):
            return instance
        else:
            return EntryForm1(self,title="NONE")
    def add_sector(self,sector:EntryForm1):
        if not sector in self.__SECTORS:
            if isinstance(sector,EntryForm1):
                self.__SECTORS.append(sector)
                return True
        return False
    def _moveX(self,index,x):
        self.update_cvs()
        sector = self._get_sector(index)
        sector.update()
        base = sector.winfo_x()
        plot = easing.TotalInExpo(50,0,0.0139,0,x,1)
        easing.easing_canvas(self.__SECTORS[index],plot,[self.__height / 6],100)
    def next(self):
        self.__select += 1
        if self.__select >= len(self.__SECTORS):
            self.__select = 0
        self.SELECT(self.__select)
    def get_index(self,instance:EntryForm1):
        try:
            return self.__SECTORS.index(instance)
        except ValueError:
            return None
    def SELECT(self,index):
        if index != self._before:
            self.draw(index,0,self.__center_y)
            self._get_sector(index).focus_force()
            self._get_sector(self._before).place_forget()
            self._moveX(index,self.__center_x * 1.5)
            self._before = index
    def draw(self,index,x,y,anchor=tk.CENTER):
        self.update_cvs()
        sector = self._get_sector(index)
        sector.place(x=x,y=y,width=self.__center_x,height=self.__height / 3,anchor=anchor)
        sector.setup()

