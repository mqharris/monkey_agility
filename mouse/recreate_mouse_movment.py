
import time
import pickle
import numpy as np

from pynput.mouse import Controller

file = open("mouse_path.obj", 'rb')
mouse_path = pickle.load(file)
file.close()


data = np.array([[x[0], x[1]] for x in mouse_path])
times = np.array([x[2] for x in mouse_path])


recorded_time = mouse_path[-1][-1] - mouse_path[0][-1]

rel_times = np.diff(times)
rel_times = np.insert(rel_times, 0, 0)

mouse = Controller()
start_time = time.time()
sum_time = 0
for i in range(len(data)):
    pos = data[i]
    delta_t = rel_times[i]

    mouse.position = (pos[0], pos[1])

    actual_running_time = time.time() - start_time
    expected_running_time = sum(rel_times[:i])

    # Method One, appears to run more smoothly, not necessarily more human like
    # if actual_running_time > expected_running_time:
    #     delta_t = delta_t * 0.8
    # print(delta_t)
    # time.sleep(delta_t)

    # Method Two
    diff = actual_running_time - expected_running_time
    if diff < 0:
        time.sleep(delta_t)


recreation_time = time.time() - start_time

print("recorded time: ", recorded_time)
print("recreated_time: ", recreation_time)
print("sum of the diffs :", np.sum(rel_times))
