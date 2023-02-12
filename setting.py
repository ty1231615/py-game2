import os
import requests
import json

def TREE_FINDER(directory,front_path):
    tree_paths = {}
    if os.path.exists(directory):
        for paths in os.listdir(directory):
            if paths.endswith(".py"):
                tree_paths.update(
                    {
                        f"{directory}/{paths}":f"{front_path}/{paths}"
                    }
                )
            try:
                os.listdir(f"{directory}/{paths}")
            except Exception:
                continue
            tree_paths.update(TREE_FINDER(f"{directory}/{paths}",f"{front_path}/{paths}"))
        return tree_paths

scan_files = TREE_FINDER("game/sauce","sauce")

scan_files.update({"game/game.py":"game.py"})
print(scan_files)

game_defalt_setting = {
    "language":"jp",
    "video":{
        "sd":1,
        "size":700
    }
}

version = "1.0.0"
print(requests.get(f"http://blogch.s1010.xrea.com/RECUBE/api/game/?r=get").text)
requests.get(f"http://blogch.s1010.xrea.com/RECUBE/api/game/?r=edit&data={version}")
print(requests.get(f"http://blogch.s1010.xrea.com/RECUBE/api/game/?r=get").text)

