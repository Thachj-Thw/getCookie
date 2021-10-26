import os
import sys


def path():
    try:
        return sys._MEIPASS
    except AttributeError:
        return os.path.abspath(".")
