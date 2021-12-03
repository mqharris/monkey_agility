import pickle
from matplotlib import pyplot as plt
import numpy as np

# file = open("mouse_path.obj", 'rb')
# mouse_path = pickle.load(file)
# file.close()


# data = np.array(mouse_path)


class Path:
    def __init__(self, data):
        self.data = data
        self.num_points = len(data)

        self.length = ((data[0][0] - data[-1][0]) ** 2 +
                       (data[0][1] - data[-1][1]) ** 2) ** (1/2)

    def get_relative_path(self):
        rel_path = [self.data[0]]
        for i in range(1, len(self.data)):
            delta_x = self.data[i][0] - self.data[i-1][0]
            delta_y = self.data[i][1] - self.data[i-1][1]
            rel_path.append([delta_x, delta_y])
        self.rel_path = rel_path

    def get_abs_path(self):
        path_data = self.rel_path
        abs_path = [self.data[0]]
        for i in range(1, len(path_data)):
            abs_x = path_data[i][0] + abs_path[i-1][0]
            abs_y = path_data[i][1] + abs_path[i-1][1]
            abs_path.append([abs_x, abs_y])
        self.abs_path = abs_path

    def get_length(self, data):
        return ((data[0][0] - data[-1][0]) ** 2 +
                (data[0][1] - data[-1][1]) ** 2) ** (1/2)
