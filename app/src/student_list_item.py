import tkinter
from tkinter import X

from app.src.Student import Student
from app.src.tooltip import CreateToolTip

NAME = 'Name: '
TIMESTAMP = 'Added:'


class StudentListItem(tkinter.Label):

    def __init__(self, parent: tkinter.Widget, student: Student, bg_color, anchor, font, justify, width):
        self.__student = student
        color = bg_color

        # call super constructor
        super().__init__(parent, text=self.__get_text(), bg=color, anchor=anchor, font=font, justify=justify, width=width)

        text = f"{TIMESTAMP} {student.timestamp}"
        if student.sent_mail:
            text += f' (Mail Invite Sent {student.sent_mail_timestamp})'
        CreateToolTip(self, text)

    def get_student(self):
        return self.__student

    def __get_text(self):
        return f"({self.__student.index + 1}) {NAME} {self.__student.name}, Issue: {self.__student.topic}"
