import os
import win32com.client 
import shutil
from pathlib import Path
import requests
import zipfile

def get_widevine():

    latest_widevine_version = requests.get("https://dl.google.com/widevine-cdm/versions.txt").text.split("\n")[-2]
    widevine_url = f"https://dl.google.com/widevine-cdm/{latest_widevine_version}-win-x64.zip"

    print("Downloading Widevine ZIP...")
    with open("widevine.zip", "wb") as widevinezip:
        widevinezip.write(requests.get(widevine_url).content)

    print("Extracting Widevine ZIP...")
    with zipfile.ZipFile("widevine.zip", "r") as archive:
        archive.extractall()

    print("Removing Widevine ZIP...")
    os.remove("widevine.zip")

    print("Creating Widevine folder structure...")
    os.makedirs("WidevineCdm\\_platform_specific\\win_x64")

    print("Moving files...")
    shutil.move("LICENSE.txt", "WidevineCdm")
    shutil.move("manifest.json", "WidevineCdm")
    shutil.move("widevinecdm.dll", "WidevineCdm\\_platform_specific\\win_x64")
    shutil.move("widevinecdm.dll.lib", "WidevineCdm\\_platform_specific\\win_x64")
    shutil.move("widevinecdm.dll.sig", "WidevineCdm\\_platform_specific\\win_x64")

    widevine_path = os.path.join(os.getcwd(), "WidevineCdm")

    return widevine_path

def get_chromium_path():

    default_lnk_path = os.path.join("C:\\Users\\", os.getlogin(),'Desktop\\Chromium.lnk')
    default_install_path = os.path.join("C:\\Users\\",os.getlogin() ,"AppData\\Local\\Chromium\\Application")

    if "Chromium_Custom_Path" in os.environ:
        return os.environ["Chromium_Custom_Path"]
    elif os.path.exists(default_lnk_path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(default_lnk_path)
        return os.path.dirname(shortcut.Targetpath)
    elif os.path.exists(default_install_path):
        return default_install_path
    else:
        while 1:
            user_input = input("Could not find Chromium installation path automatically. Please provide it manually:\n")
            if os.path.exists(user_input):
                os.environ["Chromium_Custom_Path"] = user_input
                print("Adding env variable...")
                return user_input

def get_new_widevine_path():
    os.chdir(get_chromium_path())
    os.chdir(os.listdir()[0]) 

    if not os.path.exists(os.path.join(os.getcwd(), "WidevineCdm")):
        return os.path.join(os.getcwd(), "WidevineCdm")
    else:
        return 0

def main():
    widevine_path = get_widevine()
    new_widevine_path = get_new_widevine_path()
    if new_widevine_path:
        print("Moving WidevineCdm folder...")
        shutil.copytree(widevine_path, get_new_widevine_path())
    else:
        print("Nothing to do")
    shutil.rmtree(widevine_path)

if __name__=="__main__":
    main()