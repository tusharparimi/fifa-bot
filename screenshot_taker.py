import pygetwindow as gw
import pyautogui
import keyboard
import cv2
import numpy as np
import threading
from functions import select_roi
from pathlib import Path
import matplotlib.pyplot as plt

class ScreenshotTaker():
    def __init__(self, roi):
        self.img = None
        self.roi = roi
        thread = threading.Thread(target=self.screenshot_taker, args=())
        thread.daemon = True
        thread.start()         

    def show(self):
        if not (self.img is None):
            cv_img = self.img.copy()
            cv_img = cv2.resize(cv_img, (400, 230))
            cv_img = np.uint8(cv_img)
            cv_img = cv2.Canny(cv_img, 100, 200)
            cv2.imshow('cv_img', cv_img)
            cv2.waitKey(1)
            

    def screenshot_taker(self):
        while True:
            roi = self.roi
            img = pyautogui.screenshot(region=(roi[0][0], roi[0][1], (roi[1][0]-roi[0][0]), \
                                               (roi[1][1]-roi[0][1])))
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            self.img = img
            
if __name__ == '__main__':
    roi = select_roi(game_name='fc24')
    staker = ScreenshotTaker(roi=roi)
    exit_flag = False
    while not exit_flag:
        staker.show()
        if keyboard.is_pressed('esc'):
            break 
    

