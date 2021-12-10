import math


def get_angle(data):
    # gets the angle the the path resultant vector
    # returns answers between 0 and 2*pi
    start = data[0]
    stop = data[-1]

    x_len = stop[0] - start[0]
    y_len = stop[1] - start[1]
    angle = math.atan2(y_len, x_len)
    if angle < 0:
        angle = angle + 2 * math.pi
    return angle


def rotate(data, angle):
    # requires relative path data
    # rotates the data of the path by angle radians
    # first point remains the same

    # angle = math.radians(angle)

    rotated_points = [data[0]]  # first point doesnt rotate
    for i in range(1, len(data)):
        point = data[i]
        x = point[0]
        y = point[1]

        x_hat = round(x * math.cos(angle) - y * math.sin(angle), 3)
        y_hat = round(x * math.sin(angle) + y * math.cos(angle), 3)
        rotated_points.append([x_hat, y_hat])

    return rotated_points


def scale(data, scale_factor):
    # requires relative path data
    # scales the resultant vector by scale_factor
    # the first point remains the same
    # x and y's are scaled independently

    first_point = data[0]
    data = data[1:]

    scaled_points = [[x[0] * scale_factor, x[1] * scale_factor] for x in data]

    scaled_points = [first_point] + scaled_points

    return scaled_points
