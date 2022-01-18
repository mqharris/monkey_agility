import pyautogui
import choose_obstacle
from mouse import Path
import random
import time


def choose_random_path(where_to_click, mouse_paths):
    current_mouse_position = pyautogui.position()
    distance = choose_obstacle.distance(
        current_mouse_position, where_to_click)
    low = int(0.8 * distance)
    high = int(1.2 * distance)
    paths = mouse_paths[low:high]
    flat = [item for sublist in paths for item in sublist]
    try:
        path = random.choice(flat)
        path = Path.Path(path.data, path.times)  # creates a copy
        return path
    except IndexError:
        return None


def scale_and_move(where_to_click, path, mouse_controller, percent=None):
    path.rel_path[0] = pyautogui.position()
    new_path, new_time = path.create_path_to(where_to_click)
    mouse_time = time.time()

    # move mouse to new location
    for i in range(len(new_path)):
        if percent:
            if (i/len(new_path)) > percent:
                return
        pos = new_path[i]
        delta_t = new_time[i]
        mouse_controller.position = (pos[0], pos[1])
        actual_running_time = time.time() - mouse_time
        expected_running_time = sum(new_time[:i])
        diff = actual_running_time - expected_running_time
        if diff < 0:
            time.sleep(delta_t)
