import os

import cv2
import numpy
import pyautogui
import time



class VideoWr:
    def __init__(self):
        self.SCREEN_SIZE = (1920, 1080)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None
        self.run = False

    def run_recorder(self):
        self.out = cv2.VideoWriter('output.mp4', self.fourcc, 12.0, self.SCREEN_SIZE)

        t = time.monotonic()
        while self.run and (time.monotonic() - t < 120):
            img = pyautogui.screenshot()
            frame = numpy.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.out.write(frame)
            try:
                if (os.stat('output.mp4').st_size // 100000) > 480:
                    break
            except Exception as e:
                print(e)

        self.out.release()

        cv2.destroyAllWindows()

    def destroy(self):
        self.out.release()
        self.out = None
        cv2.destroyAllWindows()
