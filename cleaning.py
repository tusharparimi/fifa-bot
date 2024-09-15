from pathlib import Path
import cv2
import os
import sys
#import numpy as np

# read and compute sift keypoints and descriptors for templates
template1_path = Path(r'.\1721616963-1830087.png')
template1 = cv2.imread(template1_path, cv2.IMREAD_GRAYSCALE)
sift = cv2.SIFT_create(contrastThreshold=0.12)
kp1, des1 = sift.detectAndCompute(template1, None)

template2_path = Path(r'.\1721359081-8094513.png')
template2 = cv2.imread(template2_path, cv2.IMREAD_GRAYSCALE)
sift = cv2.SIFT_create(contrastThreshold=0.12)
kp2, des2 = sift.detectAndCompute(template2, None)

clean_image_names = []
dir_path = Path(".\\data\\images\\")
#print(dir_path)
files = os.listdir(dir_path)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50) # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params,search_params)

for each in files:
    match_counts = 0
    #print(Path(dir_path, each))
    img = cv2.imread(Path(dir_path, each), cv2.IMREAD_GRAYSCALE)
    #print(img.shape)
    #cv2.imshow("hello", img)
    #cv2.waitKey(0)
    kp, des = sift.detectAndCompute(img, None)
    #print(des)
    #print(kp)
    template1_matched = False
    template2_matched = False

    if des is None:
        continue

    if len(des)!=0 and len(kp1) >=2 and len(kp) >=2:

        matches = flann.knnMatch(des1,des,k=2)
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

        if match_counts>=6: #len(matches)!=0:
            template1_matched = True
            #clean_image_names.append(each)
            #print(each)
            #template1_matches = cv2.drawMatchesKnn(template1, kp1, img, kp, matches,None, **draw_params)
            #if template1_matches is not None:
            #    cv2.imshow('template1 matches', template1_matches)

    if len(des)!=0 and len(kp2) >=2 and len(kp) >=2:

        matches = flann.knnMatch(des2,des,k=2)
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

        if match_counts>=6: #len(matches)!=0:
            template2_matched = True
            #clean_image_names.append(each)
            #print(each)
            #template2_matches = cv2.drawMatchesKnn(template2, kp2, img, kp, matches,None, **draw_params)
            #f template2_matches is not None:
            #   cv2.imshow('template2 matches', template2_matches)

    if template1_matched and template2_matched:
        template1_matches = cv2.drawMatchesKnn(template1, kp1, img, kp, matches,None, **draw_params)
        if template1_matches is not None:
            cv2.imshow('template1 matches', template1_matches)
            cv2.waitKey(1)
        template2_matches = cv2.drawMatchesKnn(template2, kp2, img, kp, matches,None, **draw_params)
        if template2_matches is not None:
            cv2.imshow('template2 matches', template2_matches)
            cv2.waitKey(1)

        clean_image_names.append(each)
        print(each)                



print(len(clean_image_names))
with open(Path(".\\data\\cleaned_images_2temp.txt"), "w") as txt_file:
    for name in clean_image_names:
        txt_file.write(name + "\n")
