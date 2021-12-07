import pickle
from matplotlib import pyplot as plt
import numpy as np
import utils
from path_analysis import Path, get_absolute_path


if __name__ == "__main__":
    file = open("mouse_path.obj", 'rb')
    mouse_path = pickle.load(file)
    data = np.array([[x[0], x[1]] for x in mouse_path])
    times = np.array([x[2] for x in mouse_path])

    path = Path(data, times)

    path.get_relative_path()

    xs = [x[0] for x in path.rel_path]
    ys = [y[0] for y in path.rel_path]

    plt.hist(xs[1:], density=False, bins=30)  # density=False would make counts
    plt.ylabel('delta')
    plt.xlabel('Data')
    plt.title("movements for X")
    plt.show()
