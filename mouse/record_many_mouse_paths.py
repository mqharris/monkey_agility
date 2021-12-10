import pickle
import time

from pynput.mouse import Listener

pos = []

COUNTER = 0


def on_move(x, y):
    t = time.time()
    print('Pointer moved to {0}'.format(
        (x, y, t)))
    pos.append([x, y, t])


def on_click(x, y, button, pressed):
    global pos
    global COUNTER
    t = time.time()
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y, t)))
    if not pressed and button.name == "left":
        filehandler = open(
            "./mouse_paths/mouse_path_{}.obj".format(COUNTER), "wb")
        pickle.dump(pos, filehandler)
        filehandler.close()
        pos = []
        COUNTER += 1
    if not pressed and button.name == "right":
        pos = []


# Collect events until released
with Listener(
        on_move=on_move,
        on_click=on_click
) as listener:
    listener.join()
