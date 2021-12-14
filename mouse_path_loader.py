import os.path
import os
import pickle
import numpy as np
import glob
# import utils
# import mouse
from mouse import pathClass
import re


def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


files = sorted(glob.glob(os.path.join('./mouse_paths/*')), key=numericalSort)


def load_mouse_paths(path="./mouse/mouse_paths/"):
    mouse_paths = {}
    files = sorted(glob.glob(os.path.join(
        './mouse_paths/*')), key=numericalSort)
    for file in files:
        print(file)
        if "mouse_path_" not in file:
            continue
        file = open(file, 'rb')
        mouse_path = pickle.load(file)
        mouse_path = [[x[0], x[1]] for x in mouse_path]
        times = [x[2] for x in mouse_path]
        path = pathClass.Path(mouse_path, times)
        if path.length in mouse_paths:
            mouse_paths[path.length].append(path)
        else:
            mouse_path[path.length] = [path]
        file.close()


if __name__ == "__main__":
    mouse_paths = load_mouse_paths()

    print(mouse_paths)
