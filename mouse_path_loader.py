import os.path
import os
import pickle
import mouse
import numpy as np
import glob
from mouse import pathClass
import re


def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def load_mouse_paths(path="./mouse/mouse_paths/"):
    files = sorted(glob.glob(os.path.join(path)), key=numericalSort)
    mouse_paths = {}
    files = sorted(glob.glob(os.path.join(
        './mouse/mouse_paths/*')), key=numericalSort)
    for file in files:
        if "mouse_path_" not in file:
            continue
        file = open(file, 'rb')
        mouse_path = pickle.load(file)
        data = [[x[0], x[1]] for x in mouse_path]
        times = [x[2] for x in mouse_path]
        file.close()
        if mouse_path:
            path = pathClass.Path(data, times)
        else:
            continue
        rounded_length = int(round(path.length, 0))
        if rounded_length in mouse_paths:
            mouse_paths[rounded_length].append(path)
        else:
            mouse_paths[rounded_length] = [path]
    return sort_mouse_paths(mouse_paths)


def sort_mouse_paths(mouse_paths):
    max_length = max(mouse_paths.keys())
    mouse_path_list = [[] for _ in range(max_length + 1)]
    for key, value in mouse_paths.items():
        mouse_path_list[key] = value
    return mouse_path_list


if __name__ == "__main__":
    l = load_mouse_paths()

    low = int(900 * 0.8)
    high = int(900 * 1.2)

    sub = l[low:high]
    flat = [item for sublist in sub for item in sublist]

    print(l[1001][0].length)
