import pickle
from matplotlib import pyplot as plt
import numpy as np
import utils
from path_analysis import Path, get_absolute_path

file = open("mouse_path.obj", 'rb')
mouse_path = pickle.load(file)
file.close()

fig = plt.figure()
ax = fig.add_subplot(111)


for i in range(1, 3):
    print(i)
    path = Path(mouse_path)
    path.get_relative_path()
    rotated = utils.rotate(path.rel_path, 180 * i)
    abs_rotated = get_absolute_path(rotated)
    data = np.array(abs_rotated)
    x, y = data.T
    x_r = list(x)
    y_r = list(y)
    plt.scatter(x_r, y_r)


# data = np.array(mouse_path)

# x, y = data.T

# x = list(x)
# y = list(y)

# fig = plt.figure()
# ax = fig.add_subplot(111)

# plt.scatter(x, y, marker="x")
# plt.scatter(x_r, y_r, marker="o")
# # plt.axis([1400, 1650, 200, 300])
plt.xlim(-2500, 2500)
plt.ylim(-2500, 2500)
ax.set_aspect('equal', adjustable='box')

ax = plt.gca()
ax.invert_yaxis()

plt.show()
