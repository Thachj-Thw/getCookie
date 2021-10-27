import tkinter as tk


class GetCookie(tk.Frame):
    """
    GetCookie
        - button (Button get cookie)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        self.button = ButtonGetCookie(self)

        self.pack(fill=tk.X)


class ButtonGetCookie(tk.Button):
    """Button get cookie"""
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Get Cookie", font="Arial 12", fg="#acbac2", bg=master["bg"],
                         width=10, height=1, activebackground="#484c4d", bd=0, **kwargs)
        self.dbg = master["bg"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.pack(pady=5)

    def on_enter(self, _):
        self["bg"] = self["activebackground"]

    def on_leave(self, _):
        self["bg"] = self.dbg
