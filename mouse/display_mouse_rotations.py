import pickle
from matplotlib import pyplot as plt
import numpy as np
import utils
from path_analysis import Path, get_absolute_path

file = open("mouse_path.obj", 'rb')
mouse_path = pickle.load(file)
mouse_path = [[x[0], x[1]] for x in mouse_path]
file.close()

fig = plt.figure()
ax = fig.add_subplot(111)

num_rotations = 10


for i in range(1, num_rotations + 1):
    print(i)
    path = Path(mouse_path)
    path.get_relative_path()
    rotated = utils.rotate(path.rel_path, (360/num_rotations) * i)
    abs_rotated = get_absolute_path(rotated)
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
