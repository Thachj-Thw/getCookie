import tkinter as tk


class ShowVersion(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=master["bg"], **kwargs)
        label = tk.Label(self, text="Version: 0.1.0", bg=master["bg"], font="Arial 8", fg="#acbac2")

        label.pack(side=tk.RIGHT, padx=10, pady=5)
        self.pack(fill=tk.X)
