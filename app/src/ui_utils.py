import tkinter.messagebox
from tkinter import Tk
import sys

def show_error_and_exit(error_msg, exit_code=1, before_exit=None):
    newWin = Tk()
    newWin.withdraw()
    tkinter.messagebox.showerror("Fatal Error!", f"{error_msg}\nExiting.",
              parent=newWin)
    newWin.destroy()
    print(error_msg)
    if before_exit:
        before_exit()
    sys.exit(exit_code)