from pynput.mouse import Controller
from mouse import Path
import random
import choose_obstacle
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
import utils
import argparse

TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print("torch version: ", torch.__version__)

# for pausing and resuming the main loop
PAUSE_FLAG = False
EXIT_FLAG = False

# For adding noise to click location
Y_MEAN = 6.5727
Y_STD = 7.7418

X_MEAN = -9.9818
X_STD = 8.4045

TIME_MEAN = 0.2
TIME_STD = 0.1

BETWEEN_OBSTACLES_WAIT = 5

# determines state
SEERS_TIMES = [8.3, 6.3, 9.1, 4.5, 5.35, 3.6, 9.75]
# SEERS_TIMES = [8.3, 6.5, 9.1, 4.5, 5.35, 4.2, 9.75]
# SEERS_TIMES = [x - 1 for x in SEERS_TIMES]

SEERS_NEXT_POS = [[996, 870], [997, 532],
                  [854, 456], [1108, 683], [844, 516], [156, 427], [414, 801]]


def on_press(key):
    global PAUSE_FLAG
    global EXIT_FLAG
    if key == keyboard.Key.ctrl:
        print("PAUSING")
        PAUSE_FLAG = not PAUSE_FLAG
    if key == keyboard.Key.esc:
        EXIT_FLAG = True
        PAUSE_FLAG = not PAUSE_FLAG


CONFIDENCE_THRESHOLD = 0.8

setup_logger()

if __name__ == "__main__":

    # set up env type for testing or live running
    parser = argparse.ArgumentParser(
        description="required flag for environment type")
    parser.add_argument('env_type', type=str,
                        help='test or live, depending on environemtn')
    args = parser.parse_args()
    env_type = args.env_type
    if env_type not in set(["test", "live"]):
        raise Exception("Invalid environment flag")

    # listens for exit or pause keys
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

    not_seen_counter = 0

    # for moving the mouse
    mouse_controller = Controller()

    # for machine vision model
    screen_shot_bounding_box = {'top': 0, 'left': 0,
                                'width': 1920, 'height': 1080}

    print("starting monkey agility")
    state_index = 0
    while True:
        if not PAUSE_FLAG:

            if EXIT_FLAG:
                print("exiting program")
                exit()

            start_time = time.time()

            # wait until agent stops moving for next instruction
            is_moving = True
            while is_moving:
                is_moving = is_there_movement(0.8, 0.1, sct)

            # detect obstacles in frame
            screen_data = np.array(sct.grab(screen_shot_bounding_box))
            image = cv2.cvtColor(np.array(screen_data), cv2.COLOR_RGB2BGR)
            outputs = predictor(image)

            # manage state
            seen_obstacles = outputs["instances"].get_fields()["pred_classes"]
            if (0 in seen_obstacles) and (1 in seen_obstacles):
                state_index = 0

            # get mouse's current location
            current_mouse_position = pyautogui.position()

            # get where to click
            obstacle_to_click = choose_obstacle.choose_obstacle(
                outputs["instances"].get_fields())
            if not obstacle_to_click:
                print(
                    "nothing seen, moving mouse towards the middle of the screen, counter: ", not_seen_counter)
                after_location = [825, 583]
                after_click = [after_location[0] + np.random.normal(100, 50, 1)[0],
                               after_location[1] + np.random.normal(100, 50, 1)[0]]
                percent_to_complete = np.random.normal(0.5, 0.2, 1)[0]
                print(pyautogui.position(), after_location)
                after_path = utils.choose_random_path(after_click, mouse_paths)
                if after_path:
                    utils.scale_and_move(after_click, after_path,
                                         mouse_controller, percent_to_complete)
                not_seen_counter += 1
                if not_seen_counter > 10:
                    raise Exception("Panic due to not seen counter > 10")
                continue
            obstacle_center = choose_obstacle.get_obstacle_center(
                obstacle_to_click)

            # add buffer because of the error in the edges of the mask
            volume = np.count_nonzero(obstacle_to_click["pred_masks"])
            if volume < 2000:
                scale_factor = 0.5
            else:
                scale_factor = 0.7

            # add noise to click location
            x_noise = np.random.normal(X_MEAN, X_STD, 1)[0]
            y_noise = np.random.normal(Y_MEAN, Y_STD, 1)[0]
            new_click = [int(round(obstacle_center[0] + x_noise)),
                         int(round(obstacle_center[1] + y_noise))]
            while not obstacle_to_click["pred_masks"][new_click[1]][new_click[0]]:
                print("RE DOING")
                x_noise = np.random.normal(X_MEAN, X_STD, 1)[0]
                y_noise = np.random.normal(Y_MEAN, Y_STD, 1)[0]
                new_click = [int(round(obstacle_center[0] + x_noise)),
                             int(round(obstacle_center[1] + y_noise))]
            where_to_click = new_click

            # add buffer because of the error in the edges of the mask
            mask_buffer = Path.Path([obstacle_center, where_to_click])
            mask_buffer.scale_path(scale_factor)
            shrunk_click_location = Path.get_absolute_path(
                mask_buffer.rel_path)
            where_to_click = shrunk_click_location[-1]

            # get path from current mouse position to obstacle
            path = utils.choose_random_path(where_to_click, mouse_paths)
            if not path:
                print("continuing due to no path found")
                continue
            utils.scale_and_move(where_to_click, path, mouse_controller)

            # interact with the environment
            pyautogui.click()
            if args.env_type == "test":
                print("pressing right arrow key while testing")
                pyautogui.press("right")
            after_click_wait = abs(np.random.normal(0, 0.2, 1)[0]) + 0.2
            time.sleep(after_click_wait)

            # wait between clicking and next input
            wait_timer = time.time()

            try:
                
                after_location = SEERS_NEXT_POS[state_index]
            except IndexError:
                # utils.display_prediciton(predictor, outputs)
                state_index = len(SEERS_TIMES) - 1  # fail safe

            # move the mouse after the click
            decider = random.uniform(0, 1)
            print("decider", decider)
            if decider < 0.95:
                if decider > 0.3:
                    print("towards next")
                    after_location = SEERS_NEXT_POS[state_index]
                else:
                    print("towards center")
                    after_location = [825, 583]
                after_click = [after_location[0] + np.random.normal(100, 50, 1)[0],
                               after_location[1] + np.random.normal(100, 50, 1)[0]]
                percent_to_complete = np.random.normal(0.5, 0.2, 1)[0]
                print(pyautogui.position(), after_location)
                after_path = utils.choose_random_path(after_click, mouse_paths)
                if after_path:
                    utils.scale_and_move(after_click, after_path,
                                         mouse_controller, percent_to_complete)
                else:
                    print("could not find after path, keeping mouse still")
            else:
                print("no movement according to the decider")

            # wait between obstacles
            time_needed = SEERS_TIMES[state_index]
            sleep_noise = abs(np.random.normal(TIME_MEAN, TIME_STD, 1)[0])
            time_to_sleep = time_needed - (time.time() - wait_timer)
            print("time to sleep: ", time_to_sleep,
                  "time needed: ", time_needed, "state: ", state_index)
            time_with_noise = time_to_sleep + sleep_noise
            time.sleep(time_with_noise)

            state_index += 1
            not_seen_counter = 0
