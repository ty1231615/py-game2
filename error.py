import random
from re import M
from game.sauce.lang import LangWord

class ERROR:
    __ERRORS = {
        0:{
            "name":"Unknown error",
            "detail":LangWord(jp="原因不明のエラーです",en="The reason is unknown")
        },
        1:{
            "name":"test",
            "detail":LangWord(jp="テスト",en="TEST")
        },
        2:{
            "name":"integrityError",
            "detail":LangWord(jp="このシステムは安全ではありません",en="The system is not secure.")
        },
        3:{
            "name":"AlreadyUseUserNameError",
            "detail":LangWord(jp="このユーザー名は既に使用されています",en="This user name is already in use")
        },
        4:{
            "name":"incorrectPasswordError",
            "detail":LangWord(jp="このパスワードは正しくありません",en="This password is incorrect")
        },
        5:{
            "name":"UnknownUserNameError",
            "detail":LangWord(jp="不明なユーザー名です",en="Unknown user name")
        },
        6:{
            "name":"AlreadyLoggedIn",
            "detail":LangWord(jp="このアカウントはすでにログインされています",en="this Account Already logged in")
        },
        7:{
            "name":"ExTaskConnection",
            "detail":LangWord(jp="ExTaskの接続が確認できませんでした",en="ExTask connection could not be confirmed")
        },
        8:{
            "name":"ExTaskFailure",
            "detail":LangWord(jp="登録されていないExコマンドが参照されました",en="An unregistered Ex command was referenced.")
        }
    }
    @classmethod
    def get_detail(cls,id:int,lang="en",log=None):
        if id in ERROR.__ERRORS:
            error_value = ERROR.__ERRORS[id]
            #ValueError : aaaaa
            name_value = error_value["name"]
            detail_value = error_value["detail"].get(lang)
            if log:
                detail_value = log
            print(f"[{name_value}] {detail_value}")
            return (id,name_value,detail_value)
        else:
            #入ってない場合
            print("(´・ω・`)")
            return None

