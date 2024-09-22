import controller as cn
import screenshot_taker as st
import time
import os
import cv2
import numpy as np
import functions
from pathlib import Path
import argparse
import keyboard


class DataRecorder():   
    def __init__(self):
        self.TimeStamp = 0
        self.xc_object = cn.Controller()
        self.st_object = st.ScreenshotTaker()

    def record(self, img_dir_path, csv_path):
        if not os.path.exists(img_dir_path):
            os.makedirs(img_dir_path)

        self.TimeStamp = time.time()

        cv_img = self.st_object.img
        cv_img = cv2.resize(cv_img, (400, 230))
        cv_img = np.uint8(cv_img)
        cv2.imwrite(Path(img_dir_path, \
                         str(self.TimeStamp).replace('.', '-') + '.png'), cv_img)

        dict_data = {'tstamp':self.TimeStamp, 'lx':self.xc_object.LeftJoystickX, \
                     'ly':self.xc_object.LeftJoystickY, 'a':self.xc_object.A, \
                        'b':self.xc_object.B}
        functions.log_csvfile(dict_data, csv_path)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", help="path where image file need to be stored", \
                    dest="path")
    ap.add_argument("-csvp", "--csv_path", \
                    help="path to csv file path where controller data needs to be stored", \
                        dest="csvpath")
    args = ap.parse_args()
    
    img_dir_path = Path(args.path)
    csv_file_path = Path(args.csvpath)

    data_recorder = DataRecorder()
    while True:
        data_recorder.record(img_dir_path, csv_file_path)
        if keyboard.is_pressed('esc'):
            break
        

