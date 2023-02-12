import json

path = "./setting.json"
language = "en"
video = {
    "sd":0,
    "size":0
}

def load():
    global language,video
    settings = json.loads(open(path,"r").read())
    language = settings.get("language","en")
    video = settings.get("video",{})