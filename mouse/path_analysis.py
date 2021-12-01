import pickle
from matplotlib import pyplot as plt
import numpy as np

file = open("mouse_path.obj", 'rb')
mouse_path = pickle.load(file)
file.close()


data = np.array(mouse_path)


class Path:
    def __init__(self, data):
        self.data = data
        self.num_points = len(data)

        self.length = ((data[0][0] - data[-1][0]) ** 2 +
                       (data[0][1] - data[-1][1]) ** 2) ** (1/2)
