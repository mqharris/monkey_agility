import pyautogui
import numpy as np
import time
from mss import mss


def is_there_movement(percent_matching_pixels=0.8, wait_timer=0.25):
    bounding_box = {'top': 500, 'left': 500, 'width': 400, 'height': 300}
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

    bounding_box = {'top': 500, 'left': 500, 'width': 400, 'height': 300}

    sct = mss()

    counter = 0
    old_screen = np.array(sct.grab(bounding_box))
    screen_size = old_screen.size
    while True:
        current_screen = np.array(sct.grab(bounding_box))
        number_of_matching_pixels = np.sum(old_screen == current_screen)
        print(number_of_matching_pixels, screen_size, old_screen.shape)
        if number_of_matching_pixels > (0.8 * screen_size):
            print("Not Moving")
        else:
            print("Moving")

        old_screen = current_screen

        counter += 1

        time.sleep(0.25)

        if counter % 10 == 0:
            print(counter/(time.time()-start_time))
