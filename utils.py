import pyautogui
import choose_obstacle
from mouse import Path
import random
import time
from detectron2.utils.visualizer import Visualizer, ColorMode
import numpy as np
import cv2
from mss import mss
import detectron2
import matplotlib.pyplot as plt


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


class MyVisualizer(Visualizer):
    def _jitter(self, color):
        return (.2, .71, .25)


def display_prediciton(predictor, outputs):
    sct = mss()
    ColorMode(1)
    bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
    screen_data = np.array(sct.grab(bounding_box))
    image = cv2.cvtColor(np.array(screen_data), cv2.COLOR_RGB2BGR)
    outputs = predictor(image)

    v = MyVisualizer(image,
                     metadata=detectron2.data.catalog.Metadata(name='balloon_train', thing_classes=[
                         'staging', 'obstacle'], thing_colors=[(100, 100, 100), (100, 200, 100)]),
                     scale=0.5,
                     # remove the colors of unsegmented pixels. This option is only available for segmentation models
                     instance_mode=ColorMode.SEGMENTATION
                     )
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    plt.figure(figsize=(15, 15))
    plt.imshow(out.get_image())
    plt.xticks([]), plt.yticks([])  # Hides the graph ticks and x / y axis
    plt.show()
