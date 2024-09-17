from pathlib import Path
import cv2
import os
#import sys
#import numpy as np
import argparse

# extract command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", help="mode of images (gray or edgemaps)",
                choices=['gray', 'edge'], default='gray', dest="mode")
ap.add_argument("-th", "--threshold", help="matches count threshold for cleaning",
                type=int, dest="threshold")
ap.add_argument("-nt", "--negtemplates", help="flag to use negative templates",
                dest="neg_templates", action="store_true")
ap.add_argument("-nth", "--negthreshold", help="matches count threshold for cleaning",
                type=int, dest="neg_threshold")
# print(ap.parse_args())
# print(ap.parse_args().threshold, type(ap.parse_args().threshold))
# print(ap.parse_args().neg_templates, type(ap.parse_args().neg_templates))
args = ap.parse_args()

# print(args.neg_threshold, type(args.neg_threshold))
# print(args.neg_templates, type(args.neg_templates))

if (args.neg_templates == False):
    assert (args.neg_threshold is None), "only use neg_threshold with neg_templates"

# flags
use_edgemaps = True if args.mode=="edge" else False
threshold = args.threshold
use_negtemplates = args.neg_templates
neg_threshold = args.neg_threshold
# print(use_edgemaps)
# print(threshold)
# print(use_negtemplates)
# print(neg_threshold)

# read and compute sift keypoints and descriptors for templates
templates = []
template_kp_and_des = []
for template_name in os.listdir(Path(r'.\templates'))[0:1]:
    template = cv2.Canny(cv2.imread(Path(r'.\templates', template_name), cv2.IMREAD_GRAYSCALE), 100, 200) \
        if use_edgemaps else cv2.imread(Path(r'.\templates', template_name), cv2.IMREAD_GRAYSCALE)
    templates.append(template)
    sift = cv2.SIFT_create(contrastThreshold=0.12)
    template_kp_and_des.append(sift.detectAndCompute(template, None))

neg_templates = []
neg_template_kp_and_des = []
if use_negtemplates:
    for template_name in os.listdir(Path(r'.\templates\neg')):
        template = cv2.Canny(cv2.imread(Path(r'.\templates\neg', template_name), cv2.IMREAD_GRAYSCALE), 100, 200) \
            if use_edgemaps else cv2.imread(Path(r'.\templates\neg', template_name), cv2.IMREAD_GRAYSCALE)
        neg_templates.append(template)
        sift = cv2.SIFT_create(contrastThreshold=0.12)
        neg_template_kp_and_des.append(sift.detectAndCompute(template, None))

#print(len(templates), len(neg_templates))

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
        if use_edgemaps else cv2.imread(Path(dir_path, each), cv2.IMREAD_GRAYSCALE)
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

            if match_counts >= (threshold if use_edgemaps else 6): 
                template_matched = template_matched and True
            else:
                template_matched = template_matched and False
    
    if use_negtemplates:
        for temp_kp, temp_des in neg_template_kp_and_des:
            if len(des)!=0 and len(temp_kp) >=2 and len(kp) >=2:
                neg_matches = flann.knnMatch(temp_des,des,k=2)
                neg_matchesMask = [[0,0] for i in range(len(neg_matches))]

                # ratio test as per Lowe's paper
                for i,(m,n) in enumerate(neg_matches):
                    if m.distance < 0.7*n.distance:
                        neg_matchesMask[i]=[1,0]

                match_counts = 0
                for ele in neg_matchesMask:
                    if ele == [1, 0]:
                        match_counts = match_counts + 1

                neg_draw_params = dict(matchColor = (0,255,0),
                singlePointColor = (255,0,0),
                matchesMask = neg_matchesMask,
                flags = cv2.DrawMatchesFlags_DEFAULT)

                if match_counts <= (neg_threshold if use_edgemaps else 6): 
                    template_matched = template_matched and True
                else:
                    template_matched = template_matched and False

    if template_matched:
        for i in range(len(templates)):
            template_matches = cv2.drawMatchesKnn(templates[i], template_kp_and_des[i][0], \
                                                  img, kp, matches,None, **draw_params)
            if template_matches is not None:
                cv2.imshow(f'template{i} matches', template_matches)
                cv2.waitKey(1)
        if use_negtemplates:
            for i in range(len(neg_templates)):
                template_matches = cv2.drawMatchesKnn(neg_templates[i], neg_template_kp_and_des[i][0], \
                                                    img, kp, neg_matches,None, **neg_draw_params)
                if template_matches is not None:
                    cv2.imshow(f'neg_template{i} matches', template_matches)
                    cv2.waitKey(1)
        clean_image_names.append(each)
        print(each)

# adding clean image names to a txt file
print(len(clean_image_names))
with open(Path(".\\data\\testing.txt"), "w") as txt_file:
    for name in clean_image_names:
        txt_file.write(name + "\n")   


