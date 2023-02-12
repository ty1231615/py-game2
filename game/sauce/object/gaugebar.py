import tkinter as tk

class GuageBar:
    def __init__(self,root:tk.Tk,cvs:tk.Canvas,justify=tk.LEFT) -> None:
        self.canvas = cvs
        self.root = root
        self.color = "black"
        self.size = 10
        self.width = 100
        self.height = 100
        self.__point_x = 0
        self.__point_y = 0
        self.namespace = self.__hash__()
        self.tag = f"{self.namespace}polg1"
        self.canvas.create_rectangle(self.__point_x,self.__point_y,self.__point_x,self.__point_y,fill=self.color,tag=self.tag)
    def max_count(self,count):
        self.__max = count
    def view(self,progress):
        between = self.__max_x - self.__point_x
        one = between / self.__max
        self.canvas.coords(self.tag,self.__point_x,self.__point_y - (self.size / 2),self.__point_x + (one * progress),self.__point_y + (self.size / 2))
        self.canvas.update()
    def set_max_size(self,width):
        self.__max_x = width
    def get_size(self):
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
    def set_point(self,x,y):
        self.__point_x = x
        self.__point_y = y