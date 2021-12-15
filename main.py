from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
from detectron2.utils.logger import setup_logger
import detectron2
from mouse_path_loader import load_mouse_paths
from movement_detector import is_there_movement
from pickle import load
import time
import torch
import pyautogui
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]
print(torch.__version__)


setup_logger()

if __name__ == "__main__":

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

    while True:
        start_time = time.time()

        # wait until agent stops moving for next instruction
        is_moving = True
        while is_moving:
            is_moving = is_there_movement(0.8, 0.25)
        print("agent has stopped")

        # get mouse's current location
        current_mouse_position = pyautogui.position()
        print(current_mouse_position)
