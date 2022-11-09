import os
import cv2
import numpy
import pyautogui
from win32api import GetSystemMetrics


class VideoWr:
    def __init__(self):
        self.screen_resolution = (GetSystemMetrics(0), GetSystemMetrics(1))
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None
        self.run = False

    def run_recorder(self):
        if self.screen_resolution:
            self.out = cv2.VideoWriter('output.mp4', self.fourcc, 15.0, self.screen_resolution)
        else:
            self.out = cv2.VideoWriter('output.mp4', self.fourcc, 20.0, (1920, 1080))

        while self.run:
            img = pyautogui.screenshot()
            frame = numpy.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.out.write(frame)
            if (os.stat('output.mp4').st_size // 100000) > 480:
                break

        self.out.release()

        cv2.destroyAllWindows()

    def destroy(self):
        self.out.release()
        self.out = None
        cv2.destroyAllWindows()
