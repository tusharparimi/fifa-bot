import os

# num images before cleaning
files = os.listdir(r"data\images")
print("num images before cleaning: ", num_images := len(files))

# num templates = 1
print("\nnum templates = ", 1)
# num images after cleaning
with open(r"data/cleaned_images.txt", "r") as file:
    lines = file.readlines()
    print("num images after cleaning: ", num_cleaned_images := len(lines))
# % of images removed
print("% of images removed: ", round(((num_images - num_cleaned_images)/num_images)*100, 2), " %")

# num templates = 2
print("\nnum templates = ", 2)
# num images after cleaning
with open(r"data/cleaned_images_2temp.txt", "r") as file:
    lines = file.readlines()
    print("num images after cleaning: ", num_cleaned_images_2temp := len(lines))
# % of images removed
print("% of images removed: ", round(((num_images - num_cleaned_images_2temp)/num_images)*100, 2), " %")




