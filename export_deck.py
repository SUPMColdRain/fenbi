import time
from git import Repo
from pywinauto.application import Application
from pywinauto.keyboard import send_keys


def export_deck():
    anki_path = "C:\\Program Files\\Anki\\anki.exe"
    # subprocess.Popen(anki_path)
    Application().start(anki_path)
    app = Application(backend="uia").connect(path=anki_path, title='账户1 - Anki')
    anki = app.window(title='账户1 - Anki')
    time.sleep(2)
    anki.type_keys("^e")
    anki.child_window(title='导出').type_keys("{DOWN 2}")
    anki.child_window(title='导出').type_keys("{TAB}")
    anki.child_window(title='导出').type_keys("{DOWN 11}")
    anki.child_window(title='导出').type_keys("{TAB}")
    anki.child_window(title='导出').type_keys("{SPACE}")
    anki.child_window(title='导出').type_keys("{TAB}")
    anki.child_window(title='导出').type_keys("{SPACE}")
    anki.child_window(title='导出').type_keys("{TAB}")
    anki.child_window(title='导出').type_keys("{ENTER}")
    send_keys("{ENTER 2}")
    anki.close()


def auto_git_push():
    repo = Repo(r'.git')
    repo.git.add(update=True)
    repo.index.commit("python auto update")
    g.pull()
    g.push()
    print("Successful push!")


if __name__ == '__main__':
    # export_deck()
    auto_git_push()
