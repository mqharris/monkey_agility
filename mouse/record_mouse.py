import pickle
import time

from pynput.mouse import Listener

pos = []
start_time = time.time()


def on_move(x, y):
    t = time.time()
    print('Pointer moved to {0}'.format(
        (x, y, t - start_time)))
    pos.append([x, y])


def on_click(x, y, button, pressed):
    global pos
    global start_time
    t = time.time()
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y, t - start_time)))
    if not pressed:
        filehandler = open("mouse_path.obj", "wb")
        print(pos)
        pickle.dump(pos, filehandler)
        filehandler.close()
        pos = []
        start_time = time.time()


# Collect events until released
with Listener(
        on_move=on_move,
        on_click=on_click
) as listener:
    listener.join()
