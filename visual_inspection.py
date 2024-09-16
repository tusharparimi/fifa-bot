import cv2
import os
from pathlib import Path

image_dir = Path(".\\data\\images")

txt_file_path = Path(".\\data\\cleaned_images_2temp_edgemaps_20.txt")
with open(txt_file_path, 'r') as file:
    for image_name in file:
        print(image_name)
        # print(str(Path(image_dir, image_name[:-1])))
        # print("Hello")
        img = cv2.imread(str(Path(image_dir, image_name[:-1])))
        cv2.imshow("img", img)
        cv2.waitKey(20)
