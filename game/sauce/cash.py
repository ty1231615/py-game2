import tkinter as tk
import pygame
from . import data
from . import approach
from . import setting
from .gui import EngineGUI
from .engine import button,scene,map,player,session,enemy

_root:tk.Tk = None
_server:approach.DataServerHandler = None
_cvs:tk.Canvas = None
_version = "Wait Version"
_play_cvs:tk.Canvas = None
_pygui = None
_account = None
_width = 600
_height = 500
_play_size = setting.video["size"]
font_path = "font.ttf"

home_scene = None
play_scene = None

def get_practice_scene(scn:EngineGUI,x=0,y=0):
    global play_scene
    approach.dataSendDefalt(
        data.DATA(
            approach.CODE_TYPES._GAME_SESSION_BIND,
            {
                "type":approach.CODE_TYPES._GAME_SESSION_TYPE_PRACTICE
            }
        ).encode()
    )
    session_data = approach.CreateTask(approach.CODE_TYPES._GAME_SESSION_BIND)
    play_scene = scene.Scene(scn.get_screen(),(_width,_height))
    play_scene.set_defalt_pos(x,y)
    MAP = map.NormalMap(0,0,5,30)
    MAP.setup((20,18))
    Player = player.Player(0,0,MAP,pygame.font.Font(font_path,35),1,1)
    Enemy = enemy.Enemy(MAP,5,5)
    play_scene.cog_regit(
        map=MAP,
        player=Player,
        enemy=Enemy
    )
    son = session.PracticeSession(session_data.get_value()[approach.CODE_TYPES._GAME_SESSION_ID],play_scene,scn.server.get_socket())
    scn.server.sessions.add(son)
    approach.dataSend(
        scn.server.socket,
        data.DATA(
            approach.CODE_TYPES._GAME_SESSION_START,son.id
        ).encode()
    )
    return play_scene

def get_home_scene(gui:EngineGUI):
    global home_scene
    home_scene = scene.Scene(gui.get_screen())
    home_scene.set_defalt_pos(0,0)
    home_scene.regit(
        button.ScaleButton(_width/1.4,_height*0.4,220,70,60,"Play",pygame.font.Font(font_path,35),delay=0,func=lambda: gui.set_load_scene(get_practice_scene(gui))),
        button.ScaleButton(_width/1.4,_height*0.6,220,50,20,"キャリア",pygame.font.Font(font_path,23),delay=1,func=lambda: print("HAAAAA")),
        button.ScaleButton(_width/1.4,_height*0.75,220,50,20,"オプション",pygame.font.Font(font_path,23),delay=1),
    )
    return home_scene

def exit():
    _server.disconnect()