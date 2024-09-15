import cv2
import os
import numpy as np

img1 = cv2.imread('1721359081-8094513.png', cv2.IMREAD_GRAYSCALE)
#print(img1.shape)
#cv2.imshow('img1', img1)
#cv2.waitKey(0)

sift = cv2.SIFT_create(contrastThreshold=0.12)
kp1, des1 = sift.detectAndCompute(img1, None)


clean_image_names = []
files = os.listdir('.\\data\\images\\')
for each in files:
    match_counts = 0
    img2 = cv2.imread('.\\data\\images\\' + each, cv2.IMREAD_GRAYSCALE)
    kp2, des2 = sift.detectAndCompute(img2,None)

    if len(kp2)!=0 and len(des2)!=0:

        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50) # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params,search_params)

        if len(kp1) >=2 and len(kp2) >=2:
            matches = flann.knnMatch(des1,des2,k=2)
            matchesMask = [[0,0] for i in range(len(matches))]

            # ratio test as per Lowe's paper
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.7*n.distance:
                    matchesMask[i]=[1,0]

            for ele in matchesMask:
                if ele == [1, 0]:
                    match_counts = match_counts + 1

            draw_params = dict(matchColor = (0,255,0),
            singlePointColor = (255,0,0),
            matchesMask = matchesMask,
            flags = cv2.DrawMatchesFlags_DEFAULT)

            if match_counts>=6: #len(matches)!=0:
                clean_image_names.append(each)
                print(each)
                #img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
                #if img3 is not None:
                #    cv2.imshow('img3', img3)
                #    cv2.waitKey(1)

print(len(clean_image_names))
with open(".\\data\\cleaned_images.txt", "w") as txt_file:
    for name in clean_image_names:
        txt_file.write(name + "\n")
