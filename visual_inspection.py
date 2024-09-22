import cv2
from pathlib import Path
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", help="path of image file dir", \
                default=r".\data\images", dest="path")
ap.add_argument("-tp", "--txt_path", help="path of text file with clean image file names", \
                dest="txtpath")
args = ap.parse_args()

assert args.txtpath is not None, "text file path is required"

image_dir = Path(args.path)
txt_file_path = Path(args.txtpath)

with open(txt_file_path, 'r') as file:
    for image_name in file:
        print(image_name)
        img = cv2.imread(str(Path(image_dir, image_name[:-1])))
        cv2.imshow("img", img)
        cv2.waitKey(20)
