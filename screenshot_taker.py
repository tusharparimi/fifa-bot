import pygetwindow as gw
import pyautogui
import keyboard
import cv2
import numpy as np
import threading
from functions import get_cursor_pos, tuplelist2str, str2tuplelist
from pathlib import Path

# print(gw.getAllTitles())
# #print(gw.getAllWindows())


class ScreenshotTaker():
    # WIN_SIZE = (int(2560), int(1600))
    # #WIN_SIZE = (int(), int())
    # #WIN_TITLE = 'FC 24' #'PS Remote Play'
    # WIN_TITLE = 'PS Remote Play'
    # WIN_TOPLEFT = (0, 0) #(500, 500)

    def __init__(self, win_title='PS Remote Play', win_topleft=(-6, 0), win_size=(865, 515)):

        self.img = None
        self.win_title = win_title
        self.win_topleft = win_topleft
        self.win_size = win_size
        self.roi = self.compute_roi()

        thread = threading.Thread(target=self.screenshot_taker, args=())
        thread.daemon = True
        thread.start()

    #TODO: WIP func that returns roi by manual selection or if precomputed roi in text file 
    # for given win_size and win_topleft 
    def compute_roi(self): #use_precomputed_roi=True
        roi = []
        try:
            #if use_precomputed_roi:
            with open(Path(".\\roi.txt"), 'r') as file:
                for line in file.readlines():
                    print(line)
                    print(line.split(":"))
                    #print(line.split(":")[0])
                    #print(tuplelist2str([self.win_topleft, self.win_size]))
                    if (line.split(":")[0]) == \
                        tuplelist2str([self.win_topleft, self.win_size]):
                        print(f"Used roi, detected! {line.split(":")[1][:-1]}")
                        print("To re-use roi (Press 'y'), else next (Press 'n')")
                        while True:
                            # if keyboard.is_pressed("y"):
                            #     return str2tuplelist(line.split(":")[1][:-1])
                            # if keyboard.is_pressed("n"):
                            #     break
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
            cv_img = self.img.copy() #[1280:1510, 1280-205:1280+202, :]#[625:750, 540:720, :]
            print(cv_img.shape)
            cv_img = cv2.resize(cv_img, (400, 230))
            #print(self.img)
            cv_img = np.uint8(cv_img)
            #print(cv_img.shape)
            cv_img = cv2.Canny(cv_img, 100, 200)
            #cv_img = cv2.resize(cv_img, (400, 230))
            cv2.imshow('cv_img', cv_img)
            cv2.waitKey(1)

    
    def screenshot_taker(self):
        while True:
            # fifa_window = gw.getWindowsWithTitle(ScreenshotTaker.WIN_TITLE)[0]
            # fifa_window.size = ScreenshotTaker.WIN_SIZE
            # fifa_window.topleft = ScreenshotTaker.WIN_TOPLEFT

            fifa_window = gw.getWindowsWithTitle(self.win_title)[0]
            #fifa_window.size = self.win_size
            #fifa_window.topleft = self.win_topleft
            roi = self.roi
            #print(fifa_window.size)
            # print(self.win_title)
            # print(self.win_size)
            # print(self.win_topleft)
            # print(self.roi)
            # roi = self.compute_roi(True) 
            # img = pyautogui.screenshot(region=(fifa_window.top, fifa_window.left, \
            #                                    fifa_window.width, fifa_window.height))
            # region = (left, top, width, height)
            img = pyautogui.screenshot(region=(roi[0][0], roi[0][1], (roi[1][0]-roi[0][0]), \
                                               (roi[1][1]-roi[0][1])))
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            self.img = img
            #self.img = cv2.resize(img, (1280, 800), interpolation = cv2.INTER_AREA)
            

if __name__ == '__main__':
    staker = ScreenshotTaker()
    while True:
        staker.show() 
        #staker.save_screenshot()
        pass
            

