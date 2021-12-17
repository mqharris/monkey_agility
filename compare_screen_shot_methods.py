import matplotlib.pyplot as plt
import time
import cv2
import pyautogui
from mss import mss
import numpy as np

sct = mss()
bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
screen_data = np.array(sct.grab(bounding_box))
image_mss = cv2.cvtColor(np.array(screen_data), cv2.COLOR_RGB2BGR)


screen_data = pyautogui.screenshot(region=(0, 0, 1920, 1080))
image = cv2.cvtColor(np.array(screen_data), cv2.COLOR_RGB2BGR)
image_pyautogui = image[:, :, ::-1]
# image_pyautogui = image


print(image_mss.shape)
print(image_pyautogui.shape)

print((image_pyautogui == image_mss).all())

plt.figure(figsize=(15, 15))
plt.imshow(image_pyautogui)
plt.xticks([]), plt.yticks([])  # Hides the graph ticks and x / y axis
plt.show()
