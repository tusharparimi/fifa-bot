import cv2
import os
import numpy as np
from pathlib import Path

img1 = cv2.imread(Path(r'.\templates\1721616963-1830087.png'), cv2.IMREAD_GRAYSCALE)
img1 = cv2.Canny(img1, 100, 200)
print(img1.shape)
cv2.imshow('img1', img1)
cv2.waitKey(0)

#gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT_create(contrastThreshold=0.12)
kp1, des1 = sift.detectAndCompute(img1, None)

# res = cv2.drawKeypoints(gray,kp1,img)
# cv2.imshow('res', res)
# cv2.waitKey(0)
match_counts_arr = []
files = os.listdir(Path('.\\data\\images\\'))
for each in files[:7000]:
    match_counts = 0
    #print(count)
    #count = count+1
    img2 = cv2.imread(Path('.\\data\\images\\', each), cv2.IMREAD_GRAYSCALE)
    img2 = cv2.Canny(img2, 100, 200)
    #print(img2.shape)
    kp2, des2 = sift.detectAndCompute(img2,None)

    if len(kp2)!=0 and len(des2)!=0:

        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50) # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params,search_params)

        if len(kp1) >=2 and len(kp2) >=2:
            matches = flann.knnMatch(des1,des2,k=2)
            #print(matches)
            #print(len(matches))
            #match_counts.append(len(matches))

            matchesMask = [[0,0] for i in range(len(matches))]

            
        
            # ratio test as per Lowe's paper
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.7*n.distance:
                    matchesMask[i]=[1,0]

            print("All matches: ", len(matches))
            for ele in matchesMask:
                if ele == [1, 0]:
                    print(ele)
                    match_counts = match_counts + 1
            print(match_counts)
            match_counts_arr.append(match_counts)


            draw_params = dict(matchColor = (0,255,0),
            singlePointColor = (255,0,0),
            matchesMask = matchesMask,
            flags = cv2.DrawMatchesFlags_DEFAULT)

            if len(matches)!=0:
                img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
                if img3 is not None:
                    cv2.imshow('img3', img3)#,plt.show()
                    cv2.waitKey(1)

print(np.array(match_counts_arr).shape)
print(np.array(match_counts_arr).mean())  

# RESULT for rgb: 5-8 values for threshold match_counts to clean data
# RESULT for edgemaps: 14 (mean for one test run) for threshold match_counts to clean data

