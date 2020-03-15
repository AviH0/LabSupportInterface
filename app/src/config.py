import os
import tkinter as tk

TITLE = "Settings"

CONFIG_DIRECTORY = os.path.join(os.path.curdir, 'app', 'config')
CONFIG_FILENAME = 'settings.conf'
CONFIG_FILE_PATH = os.path.join(CONFIG_DIRECTORY, CONFIG_FILENAME)

PATH_TO_CREDENETIALS = 'Credentials Location'
PATH_TO_CLIENT_SECRET = 'Client Secret Location'
SOURCE_SPREADSHEET = 'Spreadsheet Name'
SESSION_LINK = 'Link to Session'
INVITE_MSG_BODY = 'Invite Message File'
MAIL_ACCOUNT_CREDS = 'Mail Account Credentials'


class Settings:

    def __init__(self):
        self.settings = {PATH_TO_CREDENETIALS: os.path.join(os.path.curdir, 'app', 'credentials',
                                                            'Lab Support Intro2CS-273f7439f27c.json'),
                         SOURCE_SPREADSHEET: 'Sheet', SESSION_LINK: ''}

        self.new_settings = {key: None for key in self.settings.keys()}
        self.load_configurations()

    def change_settings(self, root=None):
        need_to_quit = False
        if not root:
            need_to_quit = True
            root = tk.Tk()
        root.title(TITLE)
        settings_frame = tk.Frame(root)
        index = 0
        for index, key in enumerate(self.settings.keys()):
            name = tk.Label(settings_frame, text=key, justify=tk.LEFT)
            name.grid(row=index, column=0, padx=5, sticky=tk.W, pady=10)
            value = tk.Entry(settings_frame)
            value.insert(0, self.settings[key])
            value.config(width=100)
            value.grid(row=index, column=1, sticky=tk.E)
            self.new_settings[key] = value
        settings_frame.pack(padx=20)

        def apply(save=True):
            if save:
                for key in self.new_settings:
                    self.settings[key] = self.new_settings[key].get()
                self.save_configurations()
            root.destroy()

        apply_btn = tk.Button(root, text="OK", command=apply)
        apply_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        cancel_btn = tk.Button(root, text="Cancel", command=lambda: apply(False))
        cancel_btn.pack(side=tk.RIGHT, padx=10, pady=10)

    def load_configurations(self):
        if os.path.isfile(CONFIG_FILE_PATH):
            lines = []
            with open(CONFIG_FILE_PATH, 'r') as file:
                line = file.readline()
                while line:
                    # Erase all leading and trailing white spaces:
                    line = line.strip()
                    # Find and erase comments:
                    comment = line.find('//')
                    if comment >= 0:
                        line = line[:comment]

                    if not line:
                        line = file.readline()
                        continue

                    lines.append(line)
                    line = file.readline()

            for line in lines:
                key, value = line.split('=')
                self.settings[key] = value.strip()[1:-1]
        else:
            print("Cannot find config file, falling back on default settings.")

    def save_configurations(self):
        # print("Saving configurations...")
        with open(CONFIG_FILE_PATH, 'w') as file:
            file.write(
                "// This is a config file for LabSupportClient. You may set config values as in the following "
                "example:\n// credentials location=\"path\\to\\credentials\"\n// Lines starting with '//' "
                "(and empty lines) are ignored.\n\n\n"
                "// ----------------------------------------------------------------------------------------- //"
                "\n\n")
            for key in self.settings.keys():
                file.write(key + '=' + "\"{}\"".format(self.settings[key]) + '\n')
        # print("Configurations saved.")
