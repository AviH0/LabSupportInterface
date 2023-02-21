import tkinter as tk
import time
from typing import Union

from app.src.Student import Student
from app.src.ui_utils import *

import webbrowser

class CurrentStudent(tk.Frame):
    student: Student
    status: int

    def __init__(self, parent: Union[tk.Widget, tk.Tk], **kwargs):
        # call super constructor
        super().__init__(parent, **kwargs)
        self.student: Student = None
        self.status: int = None
        self.current_student_label = tk.Label(self, font=HEADER2_FONT, anchor=tk.W, justify=tk.LEFT,
                                              wraplength=INFO_WRAPLENGTH)
        self.current_student_label.pack(side=tk.TOP, expand=True, fill='x')

        self.attached_file_link = tk.Label(self, font=LINK_FONT, anchor=tk.N, justify=tk.CENTER,
                                           wraplength=INFO_WRAPLENGTH, fg="blue", cursor="hand2")
        self.attached_file_link.pack(side=tk.TOP, expand=True, fill='x')
        self.attached_file_link.bind("<Button-1>", lambda x: self.link_callback())
        self.current_elapsed_time = tk.Label(self, font=HEADER2_FONT, anchor=tk.W, justify=tk.LEFT,
                                             wraplength=INFO_WRAPLENGTH)
        self.current_elapsed_time.pack(side = tk.BOTTOM, expand=True, fill='y')
        self.parent = parent
        self.__update_timer()

    def link_callback(self):
        webbrowser.open_new_tab(self.student.attached_file)

    def set_current(self, student: Student, status):
        self.status = status
        status_text = ''
        self.attached_file_link.configure(text='')
        if student:
            if self.status == HELPING:
                status_text = HELPING_STU_PRFX + '\n' + \
                              student.name + '\n\n' + \
                              TOPIC + '\n' + \
                              student.topic
            elif self.status == WAITING:
                status_text = WAITING_STU_PRFX + '\n' + \
                              student.name + '\n\n' + \
                              TOPIC + '\n' + \
                              student.topic
            if student.attached_file:
                self.attached_file_link.configure(text='Click To Open Attached File')


        # if status_text:
        self.current_student_label.configure(
            text=status_text)
        self.student = student


    def __update_timer(self):
        text = ''
        if self.student:
            student_last_time = (
                self.student.time_arrived if self.status == HELPING else self.student.time_called)
            if student_last_time:
                time_elapsed = time.time() - time.mktime(student_last_time)
                text = "Time Elapsed: " + time.strftime("%H:%M:%S", time.gmtime(time_elapsed))
        self.current_elapsed_time.configure(text=text)
        self.parent.after(1000, self.__update_timer)
