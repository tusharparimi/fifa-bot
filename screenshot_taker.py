import pygetwindow as gw
import pyautogui
import keyboard
import cv2
import numpy as np
import threading
from functions import get_cursor_pos, tuplelist2str, str2tuplelist
from pathlib import Path

class ScreenshotTaker():
    def __init__(self, win_title='PS Remote Play', win_topleft=(-6, 0), win_size=(865, 515)):
        self.img = None
        self.win_title = win_title
        self.win_topleft = win_topleft
        self.win_size = win_size
        self.roi = self.compute_roi()
        thread = threading.Thread(target=self.screenshot_taker, args=())
        thread.daemon = True
        thread.start()
 
    def compute_roi(self): 
        roi = []
        try:
            with open(Path(".\\roi.txt"), 'r') as file:
                for line in file.readlines():
                    if (line.split(":")[0]) == \
                        tuplelist2str([self.win_topleft, self.win_size]):
                        print(f"Used roi, detected! {line.split(":")[1][:-1]}")
                        print("To re-use roi (Press 'y'), else next (Press 'n')")
                        while True:
                            event = keyboard.read_event()
                            if event.event_type == keyboard.KEY_DOWN and event.name == 'y':
                                return str2tuplelist(line.split(":")[1][:-1])
                            if event.event_type == keyboard.KEY_DOWN and event.name == 'n':
                                break
        except FileNotFoundError:
            print("No pre-computed ROIs available or roi.txt location changed\n")


        print("Select new ROI...")
        print("Place cursor on the topleft of ROI and press 'l' to lock: ")
        keyboard.wait("l")
        x, y = get_cursor_pos() 
        print(f"({x},{y}) locked as topleft!")
        roi.append((x, y))
        print("Place cursor on the bottomright of ROI and press 'l' to lock: ")
        keyboard.wait("l")
        x, y = get_cursor_pos() 
        print(f"({x},{y}) locked as bottomright!")
        roi.append((x, y))
        print("\nTo save this roi, (Press 'y') else (Press 'n')")
        while True:
            if keyboard.is_pressed("y"):
                with open(Path(".\\roi.txt"), "a") as file:
                    file.write(tuplelist2str([self.win_topleft, self.win_size]) + ":" + \
                                tuplelist2str(roi) + "\n")
                    break
            if keyboard.is_pressed("n"):
                break
        return roi           

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
            fifa_window = gw.getWindowsWithTitle(self.win_title)[0]
            fifa_window.activate()
            roi = self.roi
            img = pyautogui.screenshot(region=(roi[0][0], roi[0][1], (roi[1][0]-roi[0][0]), \
                                               (roi[1][1]-roi[0][1])))
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            self.img = img
            
if __name__ == '__main__':
    staker = ScreenshotTaker(win_title='FC 24')
    while True:
        staker.show()
        pass
            

