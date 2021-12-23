import time
import pickle
import numpy as np
from mouse.Path import Path

from pynput.mouse import Controller

import pyautogui

file = open("./mouse/mouse_path.obj", 'rb')
mouse_path = pickle.load(file)
file.close()

# where we want our new line to end
desired_point = (1600, 900)

# unpack
data = np.array([[x[0], x[1]] for x in mouse_path])
times = np.array([x[2] for x in mouse_path])


current_mouse_position = pyautogui.position()
print(current_mouse_position)
x = current_mouse_position.x
y = current_mouse_position.y
print(x, y)

# for post-hoc comparison
recorded_time = mouse_path[-1][-1] - mouse_path[0][-1]
path = Path(mouse_path, times)
path.rel_path[0] = [x, y]
scale_factor = path.get_scale_factor(desired_point)
new_path, new_time = path.create_path_to(desired_point)
original_length = path.length
print("original_length : ", original_length)
print("scaled length : ", path.get_length(new_path))

# path2 = Path(new_path, new_time)
# tail2 = path2.data[-100:]
time_tail = new_time[-100:]
print('asdfk')

# do the movement of the new path to the desired poitn
mouse = Controller()
start_time = time.time()
sum_time = 0
automated_positions = []
for i in range(len(new_path)):
    pos = new_path[i]
    delta_t = new_time[i]

    mouse.position = (pos[0], pos[1])

    actual_running_time = time.time() - start_time
    expected_running_time = sum(new_time[:i])

    # Method Two
    diff = actual_running_time - expected_running_time
    if diff < 0:
        time.sleep(delta_t)

    automated_positions.append(pyautogui.position())


print("recreated scale length : ", path.get_length(automated_positions))
print("original time :", recorded_time, "new time :", time.time() - start_time)
print(pyautogui.position())
# print("scale_factor :", scale_factor)
