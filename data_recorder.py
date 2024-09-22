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
    def __init__(self, game_name):
        self.TimeStamp = 0
        self.xc_object = cn.Controller()
        roi = functions.select_roi(game_name)
        self.st_object = st.ScreenshotTaker(roi)

    def record(self, img_dir_path, csv_path, img_shape=(400, 230)):
        if not os.path.exists(img_dir_path):
            os.makedirs(img_dir_path)

        self.TimeStamp = time.time()

        cv_img = self.st_object.img
        if cv_img is not None:
            cv_img = cv2.resize(cv_img, img_shape)
            cv_img = np.uint8(cv_img)
            cv2.imwrite(Path(img_dir_path, \
                            str(self.TimeStamp).replace('.', '-') + '.png'), cv_img)

            dict_data = {'tstamp':self.TimeStamp, \
                        'lx':self.xc_object.LeftJoystickX, \
                        'ly':self.xc_object.LeftJoystickY, \
                            'a':self.xc_object.A, \
                            'b':self.xc_object.B}
            functions.log_csvfile(dict_data, csv_path)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", help="path where image file need to be stored", \
                    dest="path")
    ap.add_argument("-csvp", "--csv_path", \
                    help="path to csv file path where controller data needs to be stored", \
                        dest="csvpath")
    ap.add_argument("-s", "--shape", help="target (w,h) as a tuple for the saved images", \
                    dest="shape", default=(400, 230))
    ap.add_argument("-g", "--game", help="game_name for saving ROIs for future use", \
                    dest="game_name")
    args = ap.parse_args()
    
    img_dir_path = Path(args.path)
    csv_file_path = Path(args.csvpath)
    img_shape = args.shape
    game_name = args.game_name
    
    data_recorder = DataRecorder(game_name)
    while True:
        data_recorder.record(img_dir_path, csv_file_path, img_shape)
        if keyboard.is_pressed('esc'):
            break
        

