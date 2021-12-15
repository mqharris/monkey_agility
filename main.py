from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
from detectron2.utils.logger import setup_logger
import detectron2
from mouse_path_loader import load_mouse_paths
from movement_detector import is_there_movement
from pickle import load
import time
import cv2
import matplotlib.pyplot as plt
import torch
import pyautogui
from mss import mss
import numpy as np
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print(torch.__version__)

# to set colors for masking
detectron2.utils.visualizer.ColorMode(1)
# FOR TESTING
# FOR TESTING


class MyVisualizer(Visualizer):
    def _jitter(self, color):
        return (.2, .71, .25)


setup_logger()

if __name__ == "__main__":

    # 0 means pyautogui - slower but with better accuracy
    # 1 means mss - faster with lower accuracy
    screen_shot_method = 0

    # load mouse path data
    print("loading mouse paths")
    mouse_paths = load_mouse_paths()

    # load saved obstacle vision model
    print("loading detectron obstacle model")
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(
        'COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml'))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # Set threshold for this model
    cfg.MODEL.WEIGHTS = './agility_model.pth'  # Set path model .pth
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
    predictor = DefaultPredictor(cfg)

    print("starting monkey agility")
    num_iterations = 0
    while True:
        start_time = time.time()

        # wait until agent stops moving for next instruction
        is_moving = True
        while is_moving:
            is_moving = is_there_movement(0.8, 0.25)
        print("agent has stopped")

        # detect obstacles in frame

        # # 1.1s each iteration on average
        # screen_data = pyautogui.screenshot(region=(0, 0, 1920, 1080))
        # image = cv2.cvtColor(np.array(screen_data), cv2.COLOR_RGB2BGR)

        # 0.65s each iteration on average
        # but accuracy seems worse with mss()
        # sct = mss()
        # bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        # screen_data = np.array(sct.grab(bounding_box))
        # image = cv2.cvtColor(np.array(screen_data), cv2.COLOR_RGB2BGR)

        if screen_shot_method == 1:
            print("mss for screen shot method")
            sct = mss()
            bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
            screen_data = np.array(sct.grab(bounding_box))
            image = cv2.cvtColor(np.array(screen_data))
        elif screen_shot_method == 0:
            print("pyautogui for screen shot method")
            screen_data = pyautogui.screenshot(region=(0, 0, 1920, 1080))
            image = cv2.cvtColor(np.array(screen_data), cv2.COLOR_RGB2BGR)
            image = image[:, :, ::-1]

        outputs = predictor(image)

        # FOR TESTING # FOR TESTING # FOR TESTING # FOR TESTING # FOR TESTING
        # FOR TESTING # FOR TESTING # FOR TESTING # FOR TESTING # FOR TESTING
        v = MyVisualizer(
            # image # Used with mss's screen shot method
            image[:, :, ::-1],  # Used with pyautogui's screen shot method
            metadata=detectron2.data.catalog.Metadata(name='balloon_train', thing_classes=[
                'staging', 'obstacle'], thing_colors=[(100, 100, 100), (100, 200, 100)]),
            scale=0.5,
            # remove the colors of unsegmented pixels. This option is only available for segmentation models
            instance_mode=ColorMode.SEGMENTATION
        )
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

        # FOR TESTING # FOR TESTING # FOR TESTING # FOR TESTING # FOR TESTING
        plt.figure(figsize=(15, 15))
        plt.imshow(out.get_image())
        plt.xticks([]), plt.yticks([])  # Hides the graph ticks and x / y axis
        plt.show()
        # FOR TESTING # FOR TESTING # FOR TESTING # FOR TESTING # FOR TESTING
        # FOR TESTING # FOR TESTING # FOR TESTING # FOR TESTING # FOR TESTING

        centers = outputs["instances"].get_fields()["pred_boxes"].get_centers()
        print("obstacles' middle point", centers)

        # get mouse's current location
        current_mouse_position = pyautogui.position()
        print(current_mouse_position)

        print("time taken for 1 loop:", time.time() - start_time)
