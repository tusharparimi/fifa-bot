import os
from pathlib import Path

# num images before cleaning
files = os.listdir(Path(r"data\images"))
print("num images before cleaning: ", num_images := len(files))

print("\nRGB based: ---------------------------------------------------")
print("\nUsing cv2.SIFT(): >>>>>>>>>>>>>>>>>>>>>>>>>>>")

print("\nnum templates = ", 1)
# num images after cleaning
with open(Path(r"data\cleaned_images.txt"), "r") as file:
    lines = file.readlines()
    print("num images after cleaning: ", num_cleaned_images := len(lines))
# % of images removed
print("% of images removed: ", round(((num_images - num_cleaned_images)/num_images)*100, 2), " %")

print("\nnum templates = ", 2)
# num images after cleaning
with open(Path(r"data\cleaned_images_2temp_testing.txt"), "r") as file:
    lines = file.readlines()
    print("num images after cleaning: ", num_cleaned_images := len(lines))
# % of images removed
print("% of images removed: ", round(((num_images - num_cleaned_images)/num_images)*100, 2), " %")

print("\nEDGE MAP based: ---------------------------------------------------")

print("\nUsing cv2.SIFT(): >>>>>>>>>>>>>>>>>>>>>>>>>>>")

print("\nnum templates = ", 2, "match_threshold = ", 14)
# num images after cleaning
with open(Path(r"data\cleaned_images_2temp_edgemaps.txt"), "r") as file:
    lines = file.readlines()
    print("num images after cleaning: ", num_cleaned_images := len(lines))
# % of images removed
print("% of images removed: ", round(((num_images - num_cleaned_images)/num_images)*100, 2), " %")

print("\nnum templates = ", 2, ", match_threshold = ", 20)
# num images after cleaning
with open(Path(r"data\cleaned_images_2temp_edgemaps_20.txt"), "r") as file:
    lines = file.readlines()
    print("num images after cleaning: ", num_cleaned_images := len(lines))
# % of images removed
print("% of images removed: ", round(((num_images - num_cleaned_images)/num_images)*100, 2), " %")

print("\nnum templates = ", 1, ", threshold = ", 14, ", neg_templates = ", True, "num neg_templates = ", \
      1, ", neg_threshold = ", 10, )
# num images after cleaning
with open(Path(r"data\cleaned_images_temp1_th14_ntemp1_nth10_edge.txt"), "r") as file:
    lines = file.readlines()
    print("num images after cleaning: ", num_cleaned_images := len(lines))
# % of images removed
print("% of images removed: ", round(((num_images - num_cleaned_images)/num_images)*100, 2), " %")

print("\nUsing cv2.matchTemplate(): >>>>>>>>>>>>>>>>>>>")

print("\nmethod= cv2.TM_SQDIFF, threshold = 25e7")
# num images after cleaning
with open(Path(r"data\clean_images_tm_sqdiff_25e7.txt"), "r") as file:
    lines = file.readlines()
    print("num images after cleaning: ", num_cleaned_images := len(lines))
# % of images removed
print("% of images removed: ", round(((num_images - num_cleaned_images)/num_images)*100, 2), " %")


