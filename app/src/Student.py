import datetime
import re
import os

OS = os.name

is_linux = OS == 'linux' or OS == 'posix'
HEBREW = "קראטוןםפשדגכעיחלךףץתצמנהבסז"


class Student:

    def __init__(self, row, index, stu=None):
        if stu:
            self.timestamp = stu.timestamp
            self.name = stu.name
            self.topic = stu.topic
            self.status = stu.status
            self.index = stu.index
            self.mail = stu.mail
        else:
            self.timestamp = row[0]
            self.name = self.fix_hebrew(
                str(row[1]).encode(encoding='cp424', errors='replace').decode(encoding='cp424',
                                                                              errors='replace'))
            self.topic = str(row[2]).encode(encoding='cp424', errors='replace').decode(encoding='cp424',
                                                                                       errors='replace')

            self.time_made_orange = row[3]
            self.status = None
            if len(row) > 4 and row[4]:
                self.status = row[4]
            self.index = index
            self.mail = ''
            self.sent_mail = False
            if len(row) > 5:
                self.mail = row[5]
            if len(row) > 6:
                self.sent_mail = row[6] != ''

    def fix_hebrew(self, string: str):
        if not is_linux:
            return string
        words = string.split()
        fixed_words = []
        first_word = True
        rtl = False
        for word in words:
            for letter in word:
                if letter not in HEBREW:
                    fixed_words.append(word)
                    first_word = False
                    break
            else:
                rtl = first_word if first_word else rtl
                first_word = False
                fixed_words.append(word[::-1])
        if rtl:
            fixed_words = fixed_words[::-1]
        return " ".join(fixed_words)

    def should_be_red(self):
        if not self.time_made_orange:
            return False
        date_pattern = '(\d+)/(\d+)/(\d+)'
        date_result = re.search(date_pattern, self.timestamp)
        time_made_orange = self.time_made_orange.split(':')
        hours = int(time_made_orange[0].zfill(2))
        minutes = int(time_made_orange[1].zfill(2))
        if len(time_made_orange) > 2 and time_made_orange[2][-2:] == 'PM':
            hours += 12
        time_made_orange = datetime.datetime.now().replace(day=int(date_result.group(2)),
                                                           month=int(date_result.group(1)),
                                                           year=int(date_result.group(3)), hour=hours,
                                                           minute=minutes)
        return datetime.datetime.now().timestamp() - time_made_orange.timestamp() > 60 * 30
