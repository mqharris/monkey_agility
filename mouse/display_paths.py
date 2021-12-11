import os.path
import os
import pickle
from matplotlib import colors, pyplot as plt
import numpy as np
import glob
# import utils
# from path_analysis import Path, get_absolute_path

import re
numbers = re.compile(r'(\d+)')


def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


fig = plt.figure()
ax = fig.add_subplot(111)
files = sorted(glob.glob(os.path.join('./*')), key=numericalSort)
print(len(files))
num_to_plot = 6600
counter = 0
for file in files:
    print(file)
    if "mouse_path_" not in file:
        continue
    file = open(file, 'rb')
    mouse_path = pickle.load(file)
    mouse_path = [[x[0], x[1]] for x in mouse_path]
    file.close()
    data = np.array(mouse_path)
    if not mouse_path:
        continue

    x, y = data.T

    plt.scatter(x, y, marker=".", linewidth=0.002)
    counter += 1
    if counter > num_to_plot:
        break


plt.xlim(0, 1920)
plt.ylim(0, 1080)
# ax.set_aspect('equal', adjustable='box')

ax = plt.gca()
ax.invert_yaxis()
plt.show()

exit()

file = open("mouse_path.obj", 'rb')
mouse_path = pickle.load(file)
mouse_path = [[x[0], x[1]] for x in mouse_path]
file.close()

fig = plt.figure()
ax = fig.add_subplot(111)

num_rotations = 360


for i in range(1, num_rotations + 1):
    print(i)
    path = Path(mouse_path)
    path.get_relative_path()
    rotated = utils.rotate(path.rel_path, (360/num_rotations) * i)
    scaled = utils.scale(rotated, i / num_rotations)
    abs_rotated = get_absolute_path(scaled)
    data = np.array(abs_rotated)
    x, y = data.T
    x_r = list(x)
    y_r = list(y)
    plt.scatter(x_r, y_r)

plt.xlim(-2500, 2500)
plt.ylim(-2500, 2500)
ax.set_aspect('equal', adjustable='box')

ax = plt.gca()
ax.invert_yaxis()

plt.show()
