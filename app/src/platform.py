import sys


PYTHON_UPDATER_URL = 'https://github.com/AviH0/LabSupportInterface/releases/latest/download/Updater_Python.py'
PYTHON_UPDATER_FILE = 'Update.py'
PYTHON_MAIN_EXE_NAME = "LabSupportClient.py"
PYTHON_DEFAULT_URL = "https://github.com/AviH0/LabSupportInterface/releases/latest/download/LS_PYTHON.zip"

IS_ANDROID = False

if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    # Windows
    UPDATER_URL = 'https://github.com/AviH0/LabSupportInterface/releases/latest/download/Updater_Windows.exe'
    UPDATER_FILE = 'Update.exe'
    MAIN_EXE_NAME = "LabSupportClient.exe"
    DEFAULT_URL = "https://github.com/AviH0/LabSupportInterface/releases/latest/download/LS_Windows.zip"

elif sys.platform.startswith('linux'):
    from os import environ
    if "ANDROID_ARGUMENT" in environ or "ANDROID_ASSETS" in environ or "ANDROID_BOOTLOGO" in environ:
        # Android
        IS_ANDROID = True
        UPDATER_URL = PYTHON_UPDATER_URL
        UPDATER_FILE = PYTHON_UPDATER_FILE
        MAIN_EXE_NAME = PYTHON_MAIN_EXE_NAME
        DEFAULT_URL = PYTHON_DEFAULT_URL
    else:
        # Linux:
        UPDATER_URL = 'https://github.com/AviH0/LabSupportInterface/releases/latest/download/Updater_Linux'
        UPDATER_FILE = 'Update'
        MAIN_EXE_NAME = "LabSupportClient"
        DEFAULT_URL = "https://github.com/AviH0/LabSupportInterface/releases/latest/download/LS_Linux.zip"

elif sys.platform.startswith('darwin'):
    # MacOS:
    UPDATER_URL = 'https://github.com/AviH0/LabSupportInterface/releases/latest/download/Updater_MacOS'
    UPDATER_FILE = 'Update'
    MAIN_EXE_NAME = "LabSupportClient"
    DEFAULT_URL = "https://github.com/AviH0/LabSupportInterface/releases/latest/download/LS_MacOs.zip"

else:
    # Just use python
    UPDATER_URL = PYTHON_UPDATER_URL
    UPDATER_FILE = PYTHON_UPDATER_FILE
    MAIN_EXE_NAME = PYTHON_MAIN_EXE_NAME
    DEFAULT_URL = PYTHON_DEFAULT_URL
