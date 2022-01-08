import pickle

from pynput.mouse import Listener
from pynput import keyboard

clicks = []


def on_click(x, y, button, pressed):
    global clicks
    if not pressed and button.name == "left":
        clicks.append([x, y])
    if not pressed and button.name == "right":
        filehandler = open("recorded_clicks.obj", "wb")
        pickle.dump(clicks, filehandler)
        filehandler.close()
        print("saving and exiting")
        exit()


# Collect events until released
with Listener(
        # on_press=on_press,
        on_click=on_click
) as listener:
    listener.join()
