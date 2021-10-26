import tkinter as tk


class Line(tk.Canvas):
    """Draw a line"""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="#cdd1d4", height=1, highlightthickness=0, **kwargs)
        self.pack(fill=tk.X, padx=20, pady=7)
