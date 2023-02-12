import tkinter as tk
import copy

class easing:
    def __init__(self,obj:tk.Widget) -> None:
        self.__tasks = []
        self.__object = obj
    def del_task(self,id):
        if id in self.__tasks:
            self.__tasks.remove(id)
    def AllCancel(self):
        for id in self.__tasks:
            self.__object.after_cancel(id)
        self.__tasks = []
    def easingConfig(self,plot,cooltime,arg):
        clt = 0
        for i in plot:
            id = self.__object.after(
                clt,lambda: [self.__object.configure(**{arg:i}),self.del_task(id),print(i),self.__object.update()]
            )
            self.__tasks.append(id)
            clt += cooltime * clt
    @classmethod
    def inExpo(cls,time, begin, change, duration):
        return change * (time/duration)**2 + begin
    @classmethod
    def TotalInExpo(cls,flame,time,timeFlame,start,end,duration,just=True):
        pos = []
        Ntime = time
        for i in range(flame):
            pos.append(easing.inExpo(Ntime,start,end,duration))
            Ntime += timeFlame
        if just:
            pos.append(end)
        return pos
    @classmethod
    def slide_plot(cls,plot,scale):
        new = []
        for p in plot:
            new.append(p - scale)
        return new
    @classmethod
    def easing_canvas(cls,cvs:tk.Canvas,plotX,plotY,cooltime,command=None):
        c = 0
        for posy in plotY:
            cvs.update()
            dx = cvs.winfo_x()
            dy = cvs.winfo_y()
            for posx in plotX:
                cvs.after(c,lambda: cvs.place(x=dx + posx,y=dy + posy))
                cvs.update()
                c += cooltime * c
        if command:
            cvs.after(c,command)