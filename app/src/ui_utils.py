import tkinter.messagebox
from tkinter import Tk
import sys

WINDOW_SIZE = '1200x330'
LINK_FONT = ("Courier New", 12, 'underline')
HEADER2_FONT = ("Courier New", 16)
HEADER1_FONT = ("Courier New", 18, 'bold')
BODY_FONT = ("Courier New", 12)
BG = 'white'
LIST_TOPFRM_PADX = 10
FRAME_TITLE_PADX = 5
NO_SHOW_FRM_PADX = 10
INFO_TXT_PADX = 10
INFO_WRAPLENGTH = 300
BTN_FRM_WIDTH = 400
ACTION_BTN_PADX = 20
INFO_FRAME_LENGTH = 350

WAITING = 1
HELPING = 2

SEND_INVITE_MENU_OPT = 'Send Invite'

CLEAR_MENU_OPT = 'Clear Queue'

NO_CONNECTION = "-- No Connection --"

GET_INDEX_REGEX = '\((\d+)\).+'

LOAD_MENU_OPT = "Provide Assistance"
REMOVE_MENU_OPT = "Remove"
RESET_MENU_OPT = "Reset"
CALL_MENU_OPT = "Call Student"

DATETIME_FORMAT = '%H:%M'

ARRIVED_BTN_TEXT = "Student Arrived"
NO_SHOW_BTN_TEXT = "No Show"
FINISHED_BTN_TEXT = "Next Request"

WINDOW_TITLE = "Lab Support"
HELPING_STU_PRFX = "Receiving Assistance: "
WAITING_STU_PRFX = "Waiting for: "

TOPIC = 'Issue: '

NO_SHOW_LIST_TITLE = "Missed Appointments"
STUDENT_LIST_TITLE = "Waiting List"

INDEX = '({}) '


COLOR_FROM_STATUS = {'1': "yellow",
                     '2': "orange",
                     '3': "green"}


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