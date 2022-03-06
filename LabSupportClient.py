import stat
import subprocess
import sys
import os
from tkinter import Tk

import requests
from tqdm.tk import tqdm_tk as tqdm

from app.src.updates import updater
from app.src.platform import *





def fetch_updater():
    abort = [False]
    def cancel():
        abort[0] = True
        print("Aborted.")
    newWin = Tk()
    newWin.withdraw()
    print("Fetching updater... ", end='')
    r = requests.get(UPDATER_URL, stream=True)
    with open(UPDATER_FILE, 'wb') as f:
        t = tqdm(total=int(r.headers['Content-Length']), desc=f"Downloading {UPDATER_FILE}...",
                      unit='B', unit_scale=True, unit_divisor=1024, miniters=1, tk_parent=newWin, cancel_callback=cancel)
        for chunk in r.iter_content(chunk_size=1024*100):
            f.write(chunk)
            t.update(len(chunk))
            if abort[0]:
                break

        t.close()
    r.close()

    newWin.destroy()
    if abort[0]:
        exit(0)
    print("done.")

if __name__ == '__main__':
    updates_disabled = False
    if len(sys.argv) > 1:
        updates_disabled = sys.argv[1] == "--no-updates"
    if not updates_disabled and updater.check_for_updates():
        fetch_updater()
        os.chmod(UPDATER_FILE, stat.S_IXUSR | stat.S_IRUSR| stat.S_IWUSR)
        subprocess.Popen(UPDATER_FILE)
        sys.exit(0)
    from app.src import GUI
    gui = GUI.Gui()

