import os
import cv2
import numpy
import pyautogui
from win32api import GetSystemMetrics


class VideoWr:
    """
    Class Video Writer instances
    """
    def __init__(self):
        self.screen_resolution = (GetSystemMetrics(0), GetSystemMetrics(1))
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None
        self.run = False

    def run_recorder(self):
        """
        The function captures screenshots and passes them to a NumPy array.
        \nMax size file size is 50 Mb(for Telegram API limit)
        """

        if self.screen_resolution:
            self.out = cv2.VideoWriter('output.mp4', self.fourcc, 15.0, self.screen_resolution)
        else:
            # else screen_resolution is False
            self.out = cv2.VideoWriter('output.mp4', self.fourcc, 20.0, (1920, 1080))

        while self.run:
            img = numpy.array(pyautogui.screenshot())
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.out.write(frame)
            if (os.stat('output.mp4').st_size // 10**5) > 480:
                break

        self.out.release()

        cv2.destroyAllWindows()

    def destroy(self):
        """ Destroy video-writer instance and save file"""
        self.out.release()
        self.out = None
        cv2.destroyAllWindows()
