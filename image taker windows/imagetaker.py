# Citation: Rokas Balsys https://pylessons.com/Tensorflow-object-detection-grab-screen/
# and Sentdex https://github.com/Sentdex
# and Box Of Hats (https://github.com/Box-Of-Hats )

import time
import cv2
import numpy
import mss
import win32api as wapi
import glob

SCREEN_SECTION = {"top": 40, "left": 0, "width": 800, "height": 600}
DISPLAY_TIME = 1  # every second
SCT = mss.mss()
KEY_LIST = ["\b"]
FPS_CAPTURE = 1/25 # 25 fps
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    KEY_LIST.append(char)


def filepath_to_int(filepath):
    filepath = filepath.split('\\')[-1]
    filepath = filepath.split('.')[0]
    return int(filepath)


def get_last_frame():
    files = glob.glob("img/*/*.png")
    files = list(map(filepath_to_int, files))
    if len(files) == 0:
        return 0
    files.sort()
    last = files[-1]
    return last


def key_check():
    keys = []
    for key in KEY_LIST:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys


def parse_keys(keys):
    """Returns keys in a string"""
    if 'W' in keys and 'A' in keys:
        return 'WA'
    elif 'W' in keys and 'D' in keys:
        return 'WD'
    elif 'S' in keys and 'A' in keys:
        return 'SA'
    elif 'S' in keys and 'D' in keys:
        return 'SD'
    elif 'W' in keys:
        return 'W'
    elif 'S' in keys:
        return 'S'
    elif 'A' in keys:
        return 'A'
    elif 'D' in keys:
        return 'D'
    else:
        return 'N'


def save_images(images, frame_count):
    """
    Saves images to designated folder

            Parameters:
                    images: list of tuples which consist tuple
                    frame_count: integer with last frame id
    """
    for img, keys in images:
        folder = parse_keys(keys)
        frame_count += 1
        cv2.imwrite('img/' + folder + '/' + str(frame_count) + '.png', img)
    print('Images saved, frame count: ' + str(frame_count))


def main():
    start_time = time.time()
    start_time_for_fps = time.time()
    frames = 0
    frames_for_fsp = 0
    paused = True
    training_data = []
    last_frame_number = get_last_frame()

    print('Prepared press T to start, last_frame: ' + str(last_frame_number))
    while True:
        if not paused:
            # limit to 25 fps
            if time.time() - start_time > FPS_CAPTURE:
                start_time = time.time()
                img = numpy.array(SCT.grab(SCREEN_SECTION))
                training_data.append((img, key_check()))

                frames += 1
                frames_for_fsp += 1
                t_fps = time.time() - start_time_for_fps

                if t_fps >= DISPLAY_TIME:
                    print("FPS: ", frames_for_fsp / t_fps)
                    start_time_for_fps = time.time()
                    frames_for_fsp = 0

                # save images after 500 frames
                if frames % 500 == 0:
                    print('Saving ' + str(len(training_data)) + '==' + str(frames) + 'images; Last frame number: ' + str(
                        last_frame_number))
                    save_images(training_data, last_frame_number)
                    last_frame_number += frames
                    frames = 0
                    training_data = []

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('Running like a speedy gonzales!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main()
