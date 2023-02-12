import tkinter as tk
import os
import pickle
import re
import threading
import sys
import traceback
import json
from sauce import cash
from sauce.error import PTError,EOR
from sauce.gui import GUI,EngineGUI
import sauce.approach
from sauce.object.gaugebar import GuageBar
import sauce.command as command
from sauce.form import scale_atach
import sauce.account
import sauce.setting
import sauce.security as security
from sauce.lang import LangWord

server = sauce.approach.DataServerHandler()
sauce.approach._server = server
sauce.approach._socket = server.get_socket()
if os.path.exists("port.cash"):
    ads = pickle.load(open("port.cash","rb"))
else:
    ptn = re.compile("([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)|(localhost)")
    while True:
        ads = input("アクセス番号を入力してください: ")
        if ptn.match(ads):
            break
        else:
            print("○○○.○○○.○○○.○○○ の形で入力してください")
            continue
    pickle.dump(ads,open("port.cash","wb"))
print("データサーバーとの接続を行っています")
result = server.connect(ads)
if not result[0]:
    print(result[2])
    quit()

print("サーバーに接続しました")

recv_thre = threading.Thread(target=lambda: server._receive(EOR)).start()

print("設定ファイルを確認中")
if not os.path.exists(sauce.setting.path):
    print("初期設定ファイルをダウンロード中...")
    stn = sauce.approach.CreateExTask(server.get_socket(),sauce.approach.CODE_TYPES._GET_SETTING_DEFALT)
    json.dump(stn,open(sauce.setting.path,"w",encoding="UTF-8"),indent=4)
sauce.setting.load()

print("起動しました")

fileScan = security.FileScan(server.get_socket(),server)

try:
    #atach cash
    game_gui = GUI()
    game_gui.init_gui()
    cash._root = game_gui.root
    cash._server = server
    game_gui.setup_login()
    fileScanGui = security.FileScanGui(game_gui.login,game_gui.root,bg="white")
    fileScanBar = GuageBar(game_gui.root,fileScanGui)
    fileScan.set_gui(fileScanGui)
    fileScan.set_bar(fileScanBar)
    fileScanGui.place(width=game_gui.login.width,height=game_gui.login.height)
    fileScanGui.update_size()
    fileScanBar.set_max_size(fileScanGui.width / 1.25)
    fileScanBar.get_size()
    fileScanBar.set_point(fileScanGui.width / 4.2,fileScanGui.height / 3)
    server.set_fileScan(fileScan)
    fileScan.start_scan()
    game_gui.root.after(1,fileScanGui.show_title,LangWord(jp="フ ァ イ ル ス キ ャ ン 中 ...",en="F i l e  S c a n i n g ..."))
    cash._width = game_gui.get_size()[0]
    cash._height = game_gui.get_size()[1]
    game_gui.run()
    engine = EngineGUI(game_gui.get_size()[0],game_gui.get_size()[1],server)
    cash._pygui = engine
    engine.startup()
    engine.set_load_scene(cash.get_home_scene(engine))
    engine.run()
except PTError as e:
    cls = e.__class__
    log = traceback.format_exc()
    cash._root.after(0,lambda: EOR(cls,log))
server.disconnect()
sys.exit()