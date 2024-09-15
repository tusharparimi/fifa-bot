import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import threading

# print(gw.getAllTitles())
# #print(gw.getAllWindows())


class ScreenshotTaker():
    WIN_SIZE = (int(2560), int(1600))
    WIN_TITLE = 'FC 24'
    WIN_TOPLEFT = (0,0) #(500,500)

    def __init__(self):

        self.img = np.ones(shape=(int(1600), int(2560), 3))
        self.TimeStamp = 0

        thread = threading.Thread(target=self.screenshot_taker, args=())
        thread.daemon = True
        thread.start()


    def show(self):
        cv_img = self.img[1280:1510, 1280-205:1280+202, :]#[625:750, 540:720, :]
        #print(cv_img.shape)
        cv_img = cv2.resize(cv_img, (400, 230))
        cv_img = np.uint8(cv_img)
        print(cv_img.shape)
        cv_img = cv2.Canny(cv_img, 100, 200)
        cv2.imshow('cv_img', cv_img)
        cv2.waitKey(1)

    
    def screenshot_taker(self):
        while True:
            fifa_window = gw.getWindowsWithTitle(ScreenshotTaker.WIN_TITLE)[0]
            fifa_window.size = ScreenshotTaker.WIN_SIZE
            fifa_window.topleft = ScreenshotTaker.WIN_TOPLEFT

            img = pyautogui.screenshot(region=(fifa_window.top, fifa_window.left, fifa_window.width, fifa_window.height))
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            self.img = img
            #self.img = cv2.resize(img, (1280, 800), interpolation = cv2.INTER_AREA)
            

if __name__ == '__main__':
    staker = ScreenshotTaker()
    while True:
        #staker.show() 
        staker.save_screenshot()
            

