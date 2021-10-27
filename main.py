import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import threading
from modules.sele import *
from modules.path import path
from GUI.start import Start
from GUI.line import Line
from GUI.getCookie import GetCookie
from GUI.printCookie import PrintCookie
from GUI.version import ShowVersion
import time


class MainFrame(tk.Frame):
    """main interface"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.driver = Driver()
        img = (
            ImageTk.PhotoImage(Image.open(os.path.join(path(), "images", "copy.png")).resize((16, 16))),
            ImageTk.PhotoImage(Image.open(os.path.join(path(), "images", "tick.png")).resize((16, 16)))
        )
        self.start = Start(self)
        Line(self)
        self.get = GetCookie(self)
        self.show = PrintCookie(self, img)
        ShowVersion(self)

        self.start.button["command"] = self.on_start
        self.get.button["command"] = self.on_get

        self.pack()

    def on_start(self):
        self.start.button.disable()
        threading.Thread(target=self.run_start).start()

    def run_start(self):
        try:
            ok = self.start.ask_continue()
            if ok:
                kill_chrome()
                self.driver.start()
        finally:
            self.start.button.enable()

    def on_get(self):
        if self.driver.logged():
            threading.Thread(target=self.run_get).start()
        else:
            messagebox.showwarning(title="Warning", message="You need login facebook")

    def run_get(self):
        cookie = self.driver.create_cookies()
        self.show.label.set_text(cookie)
        time.sleep(1)
        self.driver.end()

    def on_close(self):
        if self.start.button.is_disable():
            messagebox.showwarning(title="Warning", message="Program is running, can't close")
        else:
            self.master.destroy()
            self.driver.end()


class Main(tk.Tk):
    """Options root"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("Get Cookie")
        icon = os.path.join(path(), "images", "icon.ico")
        self.iconbitmap(icon)
        self["bg"] = "#3c3f41"
        MainFrame(self)
        self.update_idletasks()
        x = self.winfo_screenwidth()//2 - self.winfo_width()//2
        y = self.winfo_screenheight()//2 - self.winfo_height() * 3//4
        self.geometry(f"+{x}+{y}")
        self.minsize(self.winfo_width(), self.winfo_height())


if __name__ == '__main__':
    install_driver()
    Main().mainloop()
