import tkinter as tk
from tkinter import messagebox
import psutil


class Start(tk.Frame):
    """
    Start
        - button (button start)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        self.button = StartButton(self)

        self.pack(fill=tk.X)

    @staticmethod
    def ask_continue():
        if "chrome.exe" in (proc.name() for proc in psutil.process_iter()):
            if not messagebox.askokcancel(message="This action will end the current chrome process"):
                return False
        return True


class StartButton(tk.Button):
    """Button start"""
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Start", font="Arial 14", fg="#acbac2", bg=master["bg"],
                         width=10, height=1, activebackground="#484c4d", bd=0, **kwargs)
        self.default = master["bg"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.pack(pady=10)

    def on_enter(self, _):
        if self["state"] == tk.NORMAL:
            self["bg"] = self["activebackground"]

    def on_leave(self, _):
        self["bg"] = self.default

    def disable(self):
        self["state"] = tk.DISABLED

    def enable(self):
        self["state"] = tk.NORMAL

    def is_disable(self):
        if self["state"] == tk.DISABLED:
            return True
        return False
