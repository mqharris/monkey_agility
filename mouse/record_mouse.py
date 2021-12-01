import pickle

from pynput.mouse import Listener

pos = []


def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))
    pos.append([x, y])


def on_click(x, y, button, pressed):
    global pos
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        filehandler = open("mouse_path.obj", "wb")
        print(pos)
        pickle.dump(pos, filehandler)
        filehandler.close()
        pos = []


# Collect events until released
with Listener(
        on_move=on_move,
        on_click=on_click
) as listener:
    listener.join()
