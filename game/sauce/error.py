from . import lang
from . import cash
from .form import scale_atach
import tkinter as tk

def EOR(log="PTError threw system",trackback="NONE"):
    print("Droped System Error")
    cash._server.stop()
    cash._server.disconnect()
    cash._root.update()
    size = (cash._root.winfo_width(),cash._root.winfo_height())
    cash._root.destroy()
    root = tk.Tk()
    root.title("pyGame Crash Logs")
    root.attributes("-fullscreen",True)
    root.update()
    root.focus_force()
    size = (root.winfo_width(),root.winfo_height())
    root.geometry(f"{size[0]}x{size[1]}")
    errorForm = tk.Canvas(root)
    errorForm.place(relheight=1,relwidth=1)
    errorForm.create_text(size[0] / 2,size[1] / 4,text="☢ pygame 2.0 was crashed ☢",font=("",scale_atach(errorForm,15)))
    errorForm.create_text(size[0] / 2,size[1] / 2.5,text=log,font=("",scale_atach(errorForm,30)),fill="red")
    errorForm.create_text(size[0] / 2,size[1] / 2.2,text="Please restart the game",font=("",scale_atach(errorForm,30)))
    trackbackTexts = tk.Text(errorForm)
    trackbackTexts.insert("0.0",trackback)
    trackbackTexts["state"] = tk.DISABLED
    trackbackTexts.place(anchor=tk.CENTER,x=size[0] / 2,y=size[1] / 1.4,height=size[1] / 2.5,width=size[0] / 1.2)
    root.mainloop()

errors = {
    1:{
        "detail":lang.LangWord(jp="サーバーに接続できない場合"),
        "log":lang.LangWord(jp="サーバーに接続できませんでした",en="Could not connect to server")
    },
    2:{
        "detail":lang.LangWord(jp="サーバーに既に接続している場合"),
        "log":lang.LangWord(jp="すでにサーバーに接続しています",en="Already connected to the server")
    },
    3:{
        "detail":lang.LangWord(jp="送信されたデータの整合性が確認できなかった場合"),
        "log":lang.LangWord(jp="送信されたデータの整合性が確認できませんでした",en="The integrity of the data sent could not be verified.")
    },
    4:{
        "detail":lang.LangWord(jp="受信したデータの整合性を確認できなかった場合"),
        "log":lang.LangWord(jp="受信したデータの整合性を確認できませんでした",en="Could not verify the integrity of the data received")
    },
    5:{
        "detail":lang.LangWord(jp="受信したデータの順序が間違っている場合"),
        "log":lang.LangWord(jp="受信したデータの順序が正しくありません",en="Incorrect order of received data")
    },
    6:{
        "detail":lang.LangWord(jp="内部エラー"),
        "log":lang.LangWord(jp="内部エラーによる緊急停止",en="Emergency stop due to internal error")
    }
}

def drop(id,lang="en",title=None,log=None):
    if id in errors:
        title = title
        log = log
        if not title:
           title = "ERROR"
        if not log:
            log = errors[id]["log"].get(lang)
        raise PTError(log)

class PTError(Exception):
    pass