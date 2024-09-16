from pathlib import Path
import cv2
import os
#import sys
#import numpy as np

# USE edge_maps flag
use_edge_maps = True

# read and compute sift keypoints and descriptors for templates
templates = []
template_kp_and_des = []
for template_name in os.listdir(Path(r'.\templates')):
    template = cv2.Canny(cv2.imread(Path(r'.\templates', template_name), cv2.IMREAD_GRAYSCALE), 100, 200) \
        if use_edge_maps else cv2.imread(Path(r'.\templates', template_name), cv2.IMREAD_GRAYSCALE)
    templates.append(template)
    sift = cv2.SIFT_create(contrastThreshold=0.12)
    template_kp_and_des.append(sift.detectAndCompute(template, None))

clean_image_names = []
dir_path = Path(".\\data\\images\\")
files = os.listdir(dir_path)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50) # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params,search_params)

# parsing each image, matching with templates and appending the clean image list
for each in files:
    match_counts = 0
    img = cv2.Canny(cv2.imread(Path(dir_path, each), cv2.IMREAD_GRAYSCALE), 100, 200) \
        if use_edge_maps else cv2.imread(Path(dir_path, each), cv2.IMREAD_GRAYSCALE)
    kp, des = sift.detectAndCompute(img, None)
    template_matched = True
    
    if des is None:
        continue

    for temp_kp, temp_des in template_kp_and_des:
        if len(des)!=0 and len(temp_kp) >=2 and len(kp) >=2:
            matches = flann.knnMatch(temp_des,des,k=2)
            matchesMask = [[0,0] for i in range(len(matches))]

            # ratio test as per Lowe's paper
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.7*n.distance:
                    matchesMask[i]=[1,0]

            match_counts = 0
            for ele in matchesMask:
                if ele == [1, 0]:
                    match_counts = match_counts + 1

            draw_params = dict(matchColor = (0,255,0),
            singlePointColor = (255,0,0),
            matchesMask = matchesMask,
            flags = cv2.DrawMatchesFlags_DEFAULT)

            if match_counts >= (14 if use_edge_maps else 6): 
                template_matched = template_matched and True
            else:
                template_matched = template_matched and False
    
    if template_matched:
        for i in range(len(templates)):
            template_matches = cv2.drawMatchesKnn(templates[i], template_kp_and_des[i][0], img, kp, matches,None, **draw_params)
            if template_matches is not None:
                cv2.imshow(f'template{i} matches', template_matches)
                cv2.waitKey(1)
        clean_image_names.append(each)
        print(each)

# adding clean image names to a txt file
print(len(clean_image_names))
with open(Path(".\\data\\cleaned_images_2temp_edgemaps.txt"), "w") as txt_file:
    for name in clean_image_names:
        txt_file.write(name + "\n")   


