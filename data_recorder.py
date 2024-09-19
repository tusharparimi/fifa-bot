import controller as cn
import screenshot_taker as st
import time
import os
import cv2
import numpy as np
import functions
from pathlib import Path


class DataRecorder():
    
    def __init__(self):
        self.TimeStamp = 0
        self.xc_object = cn.Controller()
        self.st_object = st.ScreenshotTaker()

    def record(self, img_dir_path, csv_path):
        if not os.path.exists(img_dir_path):
            os.makedirs(img_dir_path)

        self.TimeStamp = time.time()

        cv_img = self.st_object.img[1280:1510, 1280-205:1280+202, :] #[625:750, 540:720, :]
        cv_img = cv2.resize(cv_img, (400, 230))
        cv_img = np.uint8(cv_img)
        #cv_img = cv2.Canny(cv_img, 100, 200)
        #cv_img = cv2.resize(cv_img, (0, 0), fx = 1/4, fy = 1/4)
        cv2.imwrite(Path(img_dir_path, \
                         str(self.TimeStamp).replace('.', '-') + '.png'), cv_img)

        dict_data = {'tstamp':self.TimeStamp, 'lx':self.xc_object.LeftJoystickX, \
                     'ly':self.xc_object.LeftJoystickY, 'a':self.xc_object.A, \
                        'b':self.xc_object.B}
        functions.log_csvfile(dict_data, csv_path)

if __name__ == '__main__':
    data_recorder = DataRecorder()
    while True:
        data_recorder.record(Path('.\\data\\images1'), \
                             Path('.\\data\\controller.csv'))
        
        

