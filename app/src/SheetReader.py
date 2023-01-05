import sys
import time
from tkinter import Tk
from tkinter.messagebox import showerror
from typing import Union

import app.src.config
from app.src.ui_utils import show_error_and_exit



try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import httplib2
    import requests
except ImportError:
    show_error_and_exit("Please ensure you have the packages: oauth2client, gspread installed before using.\n"
          "you can install them by pasting the following command into your shell:\n"
          "python -m pip install gspread oauth2client")


# Share spreadsheet with following email address: lab-support@lab-support-intro2cs.iam.gserviceaccount.com
# Then paste the name of the spreadsheet in the following variable:



def authenticate(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except gspread.exceptions.APIError:
            args[0].reauth()
            return inner(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            print("Connection error, please check network connection.", file=sys.stderr)
        except AttributeError:
            args[0].reauth()
            return inner(*args, **kwargs)
    return inner


class SheetReader:
    FINISHED = '3'
    NO_SHOW = '2'
    ARRIVED = '1'
    DEFAULT = ''

    QUEUE_ROW_OFFSET = 5

    def __init__(self, settings, close_callback=None):

        self.CREDENTIALS_DIRECTORY = settings.settings[
            app.src.config.PATH_TO_CREDENETIALS]  # 'app/credentials/Lab Support Intro2CS-273f7439f27c.json'
        self.NAME_OF_SPREADSHEET = settings.settings[
            app.src.config.SOURCE_SPREADSHEET]  # "Intro2CS - Lab Support Queue - Edit"

        self.on_close = close_callback

        # use creds to create a client to interact with the Google Drive API
        self.scope = ['https://www.googleapis.com/auth/drive']
        self.sheet: Union[gspread.Worksheet, None] = None
        self.client = None
        self.creds = None
        self.reinitialize()


    def reauth(self):
        if self.client and self.sheet:
            self.client = gspread.authorize(self.creds)
            self.sheet = self.client.open(self.NAME_OF_SPREADSHEET).get_worksheet(1)
            return
        self.reinitialize()

    def reinitialize(self):
        try:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_DIRECTORY, self.scope)
            self.client = gspread.authorize(self.creds)
            # Find a workbook by name and open the second sheet
            # Make sure you use the right name here.
            self.sheet = self.client.open(self.NAME_OF_SPREADSHEET).get_worksheet(1)
        except FileNotFoundError:
            show_error_and_exit("Please ensure credential files are present in credentials directory", before_exit=self.on_close)
        except gspread.exceptions.APIError:
            show_error_and_exit("Unexpected authorization error.", before_exit=self.on_close)
        except httplib2.ServerNotFoundError:
            print("Connection error, please check network connection.", file=sys.stderr)
        except requests.exceptions.ConnectionError:
            print("Connection error, please check network connection.", file=sys.stderr)

    @authenticate
    def get_current_rows(self):
        try:
            result = self.sheet.get_all_values()[4:]
            return list(filter(lambda x: x[0], result))
        except httplib2.ServerNotFoundError:
            print("Connection error, please check network connection.", file=sys.stderr)
            return None

    @authenticate
    def stu_finished(self, index):
        self.sheet.update_cell(self.__stu_index_to_row_index(index), 5, self.FINISHED)
        self.sheet.update_cell(self.__stu_index_to_row_index(index), 10, f"Turned Green at: {time.asctime()}")

    @authenticate
    def stu_no_showed(self, index, time):
        self.sheet.update_cell(self.__stu_index_to_row_index(index), 5, self.NO_SHOW)
        self.sheet.update_cell(self.__stu_index_to_row_index(index), 4, time)

    @authenticate
    def reset_stu(self, index):
        self.sheet.update_cell(5 + index, 5, self.DEFAULT)
        self.sheet.update_cell(5 + index, 4, self.DEFAULT)

    @authenticate
    def mail_sent(self, index):
        self.sheet.update_cell(self.__stu_index_to_row_index(index), 7,
                               f"SENT AT {time.strftime('%H:%M', time.localtime())}")

    @authenticate
    def call_stu(self, index):
        self.sheet.update_cell(self.__stu_index_to_row_index(index), 5, self.ARRIVED)
        self.sheet.update_cell(self.__stu_index_to_row_index(index), 8, f"Turned Yellow at: {time.asctime()}")

    @authenticate
    def stu_arrived(self, index):
        self.sheet.update_cell(self.__stu_index_to_row_index(index), 5, self.ARRIVED)
        self.sheet.update_cell(self.__stu_index_to_row_index(index), 9, f"Arrived at: {time.asctime()}")

    @authenticate
    def clear_sheet(self, rows):
        self.sheet.delete_rows(self.__stu_index_to_row_index(0), self.__stu_index_to_row_index(0) + rows)
        self.sheet.append_rows([[]]*rows)

    def __stu_index_to_row_index(self, index):
        return self.QUEUE_ROW_OFFSET + index

    @authenticate
    def remove_stu(self, index):
        self.sheet.delete_rows(self.__stu_index_to_row_index(index))
        self.sheet.append_row([])

