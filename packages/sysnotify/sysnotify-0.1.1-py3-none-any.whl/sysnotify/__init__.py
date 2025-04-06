from enum import Enum
from tkinter import Tk, Label
from plyer import notification
from tkinter import messagebox
from winsound import PlaySound
from pyttsx3 import init as pyttsx3_init

pyttsx3_engine = pyttsx3_init()
TK_FONT = ("Microsoft YaHei", 20)


def toast(title: str, msg: str, timeout: int = 10, icon=None):
    notification.notify(
        title=title,
        message=msg,
        timeout=timeout,
        app_icon=icon if icon else "sysnotify.ico",
    )


def msgbox_info(title: str, msg: str):
    messagebox.showinfo(title, msg)


def msgbox_warning(title: str, msg: str):
    messagebox.showwarning(title, msg)


def msgbox_error(title: str, msg: str):
    messagebox.showerror(title, msg)


def say(msg: str):
    pyttsx3_engine.say(msg)
    pyttsx3_engine.runAndWait()


def show_banner(msg: str, timeout: int = 5):
    root = Tk()
    root.overrideredirect(True)  # 无边框窗口
    Label(root, text=msg, font=TK_FONT).pack()
    root.after(timeout * 1000, root.destroy)  # 自动关闭
    root.mainloop()


class SystemSound(Enum):
    SYSTEM_ASTERISK = "SystemAsterisk"
    SYSTEM_EXCLAMATION = "SystemExclamation"
    SYSTEM_EXIT = "SystemExit"
    SYSTEM_HAND = "SystemHand"
    SYSTEM_QUESTION = "SystemQuestion"
    SYSTEM_START = "SystemStart"
    SYSTEM_DEFAULT = "SystemDefault"


def sys_sound(sound: SystemSound):
    PlaySound(sound, 1)  # SND_ASYNC
