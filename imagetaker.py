# Thanks to Rokas Balsys for code inspiration https://pylessons.com/Tensorflow-object-detection-grab-screen/

import time
import cv2
import numpy
from PIL import ImageGrab, Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import keyboard

START_TIME = time.time()
fps = 0
SCREEN_SECTION = (0, 40, 800, 640)
DISPLAY_TIME = 1  # every second

while True:
    img = numpy.asarray(ImageGrab.grab(bbox=SCREEN_SECTION))
    im = Image.fromarray(img)
    im.save('test.png')
    print(keyboard.read_key())
    fps += 1
    t = time.time() - START_TIME
    if t >= DISPLAY_TIME:
        print("FPS: ", fps / t)
        # set fps again to zero
        fps = 0
        # set start time to current time again
        START_TIME = time.time()

# imgplot = plt.imshow(img)
# plt.show()
