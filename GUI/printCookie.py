import tkinter as tk
import threading
import time


class PrintCookie(tk.LabelFrame):
    """
    PrintCookie
        - label (text show cookie)
        - button.button (button copy)
    """
    def __init__(self, master, img: tuple, **kwargs):
        super().__init__(master, text="Cookie", fg="#acbac2", bd=1, relief=tk.SOLID, bg=master["bg"], **kwargs)
        self.frame = tk.Frame(self, bg="#676e70")
        self.label = Show(self.frame)
        self.button = ButtonCopy(self.frame, img)
        self.button.button["command"] = self.on_click

        self.frame.pack(padx=5, pady=5)
        self.pack(fill=tk.X, padx=5, pady=5)

    def on_click(self):
        self.button.change_icon()
        self.label.copy()


class Show(tk.Text):
    """Text show cookie"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], fg="#d7dde0", bd=0, width=70, height=10, font="Arial 9", **kwargs)
        self["state"] = tk.DISABLED

        self.pack(side=tk.LEFT, padx=5, pady=5)

    def set_text(self, text):
        self["state"] = tk.NORMAL
        self.delete(1.0, tk.END)
        self.insert(1.0, text)
        self["state"] = tk.DISABLED

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.get(1.0, tk.END)[:-1])


class ButtonCopy(tk.Frame):
    """Button copy"""
    def __init__(self, master, img, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        self.button = tk.Button(self, bg=master["bg"], bd=0, activebackground=master["bg"], **kwargs)
        self.img_copy = img[0]
        self.img_tick = img[1]
        self.button["image"] = self.img_copy
        self.button.image = self.img_copy
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

        self.button.pack(side=tk.TOP, padx=5, pady=2)
        self.pack(side=tk.RIGHT, fill=tk.Y)

    def change_icon(self):
        self.button["image"] = self.img_tick
        threading.Thread(target=self.change_back).start()

    def change_back(self):
        time.sleep(1)
        self.button["image"] = self.img_copy

    def on_enter(self, _):
        self.info = Info(self)
        self.info.geometry(f"+{self.winfo_rootx()}+{self.winfo_rooty()+self.button.winfo_height()+10}")

    def on_leave(self, _):
        self.info.destroy()


class Info(tk.Toplevel):
    """Show info button copy"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="#000000", **kwargs)
        self.overrideredirect(True)
        self.label = tk.Label(self, text="Copy", bg="#ffffff")
        self.lift()

        self.label.pack(padx=1, pady=1)
