from pynput.keyboard import Key, Listener
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
from detectron2.utils.logger import setup_logger
from mouse_path_loader import load_mouse_paths
from movement_detector import is_there_movement
import time
import cv2
import torch
import pyautogui
from mss import mss
import numpy as np
from pynput import keyboard
import choose_obstacle
import random
from mouse import Path
from pynput.mouse import Controller
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print("torch version: ", torch.__version__)

# for pausing and resuming the main loop
PAUSE_FLAG = False
EXIT_FLAG = False


def on_press(key):
    global PAUSE_FLAG
    global EXIT_FLAG
    if key == keyboard.Key.ctrl:
        PAUSE_FLAG = not PAUSE_FLAG
    if key == keyboard.Key.esc:
        EXIT_FLAG = True
        PAUSE_FLAG = not PAUSE_FLAG


CONFIDENCE_THRESHOLD = 0.8

setup_logger()

if __name__ == "__main__":

    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()

    # used for mss method and is_moving()
    sct = mss()

    # load mouse path data
    print("loading mouse paths")
    mouse_paths = load_mouse_paths()

    # load saved obstacle vision model
    print("loading detectron obstacle model")
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(
        'COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml'))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = CONFIDENCE_THRESHOLD
    cfg.MODEL.WEIGHTS = './agility_model.pth'  # Set path model .pth
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
    predictor = DefaultPredictor(cfg)

    mouse_controller = Controller()

    print("starting monkey agility")
    num_iterations = 0
    while True:
        if not PAUSE_FLAG:

            if EXIT_FLAG:
                print("exiting program")
                exit()

            start_time = time.time()

            # wait until agent stops moving for next instruction
            is_moving = True
            while is_moving:
                is_moving = is_there_movement(0.8, 0.25, sct)

            # detect obstacles in frame
            bounding_box = {'top': 0, 'left': 0,
                            'width': 1920, 'height': 1080}
            screen_data = np.array(sct.grab(bounding_box))
            image = cv2.cvtColor(np.array(screen_data), cv2.COLOR_RGB2BGR)
            outputs = predictor(image)
            centers = outputs["instances"].get_fields()[
                "pred_boxes"].get_centers()
            print("obstacles' middle point", centers)

            # get mouse's current location
            current_mouse_position = pyautogui.position()

            # get where to click
            obstacle_to_click = choose_obstacle.choose_obstacle(
                outputs["instances"].get_fields())
            where_to_click = choose_obstacle.get_click_location(
                obstacle_to_click)
            print("current mouse location : {}, move mouse to : {}".format(
                current_mouse_position, where_to_click))

            # choose a mouse path
            distance = choose_obstacle.distance(
                current_mouse_position, where_to_click)
            low = int(0.8 * distance)
            high = int(1.2 * distance)
            paths = mouse_paths[low:high]
            flat = [item for sublist in paths for item in sublist]
            try:
                path = random.choice(flat)
                # create a copy
                path = Path.Path(path.data, path.times)
            except IndexError:
                print("continuing due to no path found")
                continue

            # scale and rotate to new location
            path.rel_path[0] = current_mouse_position
            new_path, new_time = path.create_path_to(where_to_click)
            mouse_time = time.time()

            # move mouse to new location
            for i in range(len(new_path)):
                pos = new_path[i]
                delta_t = new_time[i]
                mouse_controller.position = (pos[0], pos[1])
                actual_running_time = time.time() - mouse_time
                expected_running_time = sum(new_time[:i])
                diff = actual_running_time - expected_running_time
                if diff < 0:
                    time.sleep(delta_t)

            # pyautogui.click()
            pyautogui.press("right")

            time.sleep(0.33)

            print("time taken for 1 loop:", time.time() - start_time)
