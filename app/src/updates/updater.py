import shutil
import requests
import zipfile
import os
import json

from tqdm import tqdm
from app.src.platform import *

UPDATE_FILE = 'update.zip'

TEMP_DIR = ".update_data"
ARCHIVE_ROOT_NAME = ""
INF_JSON_URL = "https://raw.githubusercontent.com/AviH0/LabSupportInterface/master/app/src/updates/inf.json"


def do_update():
    if __is_update_needed():
        print("Updating LabSupportClient...\n")
        __download_update()
        __extract_update()
        __copy_update()
        __clean_up()
        print("Update successful.")
        os.execv(MAIN_EXE_NAME, ['a'])
        return True
    else:
        return False


def check_for_updates():

    if __is_update_needed():
        return True


def __is_update_needed():
    print("checking for updates...")
    try:
        with open("app/src/updates/inf.json") as inf:
            product_info = json.load(inf)
            r = requests.get(INF_JSON_URL)
            newest_info = r.json()
            installed_version = product_info["version"].split('.')
            newest_version = newest_info["version"].split('.')
            if __compare_versions(installed_version, newest_version):
                print("newer version found.")
                return True
    except json.JSONDecodeError:
        print("Problem identifying current version")
        return True
    except FileNotFoundError:
        print("Problem identifying current version")
        return True
    except requests.ConnectionError:
        print("Could not connect to update server.")
        return False
    print("Installed version is up-to-date.")
    return False


def __compare_versions(installed_version, newest_version):
    if int(installed_version[0]) < int(newest_version[0]):
        return True
    if int(installed_version[1]) < int(newest_version[1]):
        return True
    if int(installed_version[2]) < int(newest_version[2]):
        return True
    return False


def __download_update():
    print("Fetching update... ", end='')
    with requests.get(DEFAULT_URL, stream=True) as r:
        with open(UPDATE_FILE, 'wb') as f:
            t = tqdm(total=int(r.headers['Content-Length']), desc=f"Downloading {UPDATE_FILE}...",
                          unit='B', unit_scale=True, unit_divisor=1024, miniters=1)
            for chunk in r.iter_content(chunk_size=1024 * 100):
                f.write(chunk)
                t.update(len(chunk))
            t.close()
        # with open(UPDATE_FILE, 'wb') as f:
        #     # for chunk in r.iter_content(chunk_size=1024*10):
        #     #     f.write(chunk)
        #     shutil.copyfileobj(r.raw, f, length=1024*1024)
    print("done.")


def __extract_update():
    print("Extracting... ", end='')
    with zipfile.ZipFile(UPDATE_FILE, 'r') as zip_ref:
        zip_ref.extractall(TEMP_DIR)
    print("done.")


def __copy_update():
    print("Copying... ", end='')
    __recursive_overwrite(os.path.join(TEMP_DIR, ARCHIVE_ROOT_NAME), ".")
    print("done.")


def __clean_up():
    print("Removing update files... ", end='')
    if os.path.isfile("updater.py"):
        os.remove("updater.py")
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.remove(UPDATE_FILE)
    print("done.")


def __recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                __recursive_overwrite(os.path.join(src, f),
                                      os.path.join(dest, f),
                                      ignore)
    else:
        shutil.copyfile(src, dest)
