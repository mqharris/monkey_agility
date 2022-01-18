import pyautogui
import numpy as np
import time
from mss import mss
from matplotlib import pyplot as plt
from PIL import Image
import cv2


def is_there_movement(percent_matching_pixels=0.8, wait_timer=0.25, sct=None):
    bounding_box = {'top': 500, 'left': 500, 'width': 400, 'height': 300}
    if not sct:
        sct = mss()
    old_screen = np.array(sct.grab(bounding_box))
    screen_size = old_screen.size
    while True:
        time.sleep(wait_timer)
        current_screen = np.array(sct.grab(bounding_box))
        number_of_matching_pixels = np.sum(old_screen == current_screen)
        if number_of_matching_pixels > (percent_matching_pixels * screen_size):
            return False
        old_screen = current_screen


if __name__ == "__main__":

    start_time = time.time()

    bounding_box = {'top': 500, 'left': 1000, 'width': 75, 'height': 100}

    sct = mss()

    counter = 0
    while True:
        old_screen = sct.grab(bounding_box)
        screen_size = old_screen.size
        image = Image.frombytes("RGB", old_screen.size,
                                old_screen.bgra, "raw", "BGRX")

        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imshow('image', image)
        cv2.waitKey(1)
        # exit()
