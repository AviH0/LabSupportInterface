

import sys

IS_ANDROID = False

if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    # Windows
    UPDATER_URL = 'https://github.com/AviH0/LabSupportInterface/releases/download/Latest/Updater_Windows.exe'
    UPDATER_FILE = 'Update.exe'
    MAIN_EXE_NAME = "LabSupportClient.exe"
    DEFAULT_URL = "https://github.com/AviH0/LabSupportInterface/releases/download/Latest/LS_Windows.zip"

elif sys.platform.startswith('linux'):
    from os import environ
    if "ANDROID_ARGUMENT" in environ or "ANDROID_ASSETS" in environ or "ANDROID_BOOTLOGO" in environ:
        # Android
        IS_ANDROID = True
        UPDATER_URL = 'https://github.com/AviH0/LabSupportInterface/archive/refs/tags/Latest.zip'
        UPDATER_FILE = 'python3 Update.py'
        MAIN_EXE_NAME = "python3 LabSupportClient.py"
        DEFAULT_URL = "https://github.com/AviH0/LabSupportInterface/archive/refs/tags/Latest.zip"

    # Linux:
    UPDATER_URL = 'https://github.com/AviH0/LabSupportInterface/releases/download/Latest/Updater_Linux'
    UPDATER_FILE = 'Update'
    MAIN_EXE_NAME = "LabSupportClient"
    DEFAULT_URL = "https://github.com/AviH0/LabSupportInterface/releases/download/Latest/LS_Linux.zip"
elif sys.platform.startswith('darwin'):
    # MacOS:
    UPDATER_URL = 'https://github.com/AviH0/LabSupportInterface/releases/download/Latest/Updater_MacOS'
    UPDATER_FILE = 'Update'
    MAIN_EXE_NAME = "LabSupportClient"
    DEFAULT_URL = "https://github.com/AviH0/LabSupportInterface/releases/download/Latest/LS_MacOs.zip"