import numpy as np
import utils


class Path:
    def __init__(self, data, times=None):
        self.data = data
        self.num_points = len(data)
        self.length = ((data[0][0] - data[-1][0]) ** 2 +
                       (data[0][1] - data[-1][1]) ** 2) ** (1/2)
        self.times = times
        self.modified_path = None
        self.get_relative_path()

    def get_rel_times(self):
        rel_times = np.diff(self.times)
        rel_times = np.insert(rel_times, 0, 0)

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

    def rotate_path(self, rotation_amount):
        if self.modified_path:
            data = self.modified_path
        else:
            data = self.rel_path
        self.rel_path = utils.rotate(data, rotation_amount)

    def scale_path(self, scale_factor):
        if self.modified_path:
            data = self.modified_path
        else:
            data = self.rel_path
        self.rel_path = utils.scale(data, scale_factor)

    def create_path_to(self, desired_point):

        # get angle of rotation (will be negative becuase x-axis is inverted)
        rew_resultant = [self.rel_path[0], desired_point]
        new_angle = utils.get_angle(rew_resultant)
        old_angle = utils.get_angle(self.data)
        # this is backwards from expected becuase the y-axis has been flipped
        # i.e the origin is in the top left rather than the bottom left
        rotation_angle = new_angle - old_angle

        # get scale factor
        original_length = self.get_length(self.data)
        new_length = self.get_length([self.data[0], desired_point])

        print(original_length, new_length)
        scale_factor = new_length / original_length

        # rotate path
        self.rotate_path(rotation_angle)
        print(self.rel_path)

        # scale path
        self.scale_path(scale_factor)

        # get abs path
        fuck = get_absolute_path(self.rel_path)
        print(fuck)

        # return path


def get_absolute_path(path_data):
    path_data = path_data
    abs_path = [path_data[0]]
    for i in range(1, len(path_data)):
        abs_x = path_data[i][0] + abs_path[i-1][0]
        abs_y = path_data[i][1] + abs_path[i-1][1]
        abs_path.append([abs_x, abs_y])
    return abs_path
