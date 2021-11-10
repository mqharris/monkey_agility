
import pyautogui

import torch
TORCH_VERSION = ".".join(torch.__version__.split(".")[:2])
CUDA_VERSION = torch.__version__.split("+")[-1]

# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random, time
import matplotlib.pyplot as plt
# from google.colab.patches import cv2_imshow

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.data import MetadataCatalog, DatasetCatalog

# to set colors for masking
detectron2.utils.visualizer.ColorMode(1)
class MyVisualizer(Visualizer):
    def _jitter(self, color):
        return (.2, .71, .25)

# load saved model
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file('COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml'))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 # Set threshold for this model
cfg.MODEL.WEIGHTS = './agility_model.pth' # Set path model .pth
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
predictor = DefaultPredictor(cfg)



pil_image = pyautogui.screenshot(region=(0, 0, 1920, 1080))
im = np.array(pil_image)
im = im[:, :, ::-1].copy() # to convert to BGR before predicting, then again after
outputs = predictor(im)

v = MyVisualizer(
                im[:, :, ::-1],
                # im,
                metadata=detectron2.data.catalog.Metadata(name='balloon_train', thing_classes=['staging', 'obstacle'], thing_colors=[(100,100,100), (100, 200, 100)]), 
                # scale=0.5,
                scale=1, 
                instance_mode=ColorMode.SEGMENTATION   # remove the colors of unsegmented pixels. This option is only available for segmentation models
)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

# plt.figure(figsize=(15,15))
plt.imshow(out.get_image())
plt.xticks([]), plt.yticks([])  # Hides the graph ticks and x / y axis
# plt.show()
plt.savefig("./test")
plt.close()


print("aslkdfjals")
outputs["instances"].get_fields()["pred_boxes"].get_centers()
outputs["instances"].get_fields()["pred_boxes"].tensor
# myScreenshot.save("test.png")
