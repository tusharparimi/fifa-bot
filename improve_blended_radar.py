#trying to make the blended radar more visible during game (if possible)

import cv2
import numpy as np

#image = cv2.imread('.\\data\\images\\1721154781-443667.png')
image = cv2.imread('.\\data\\images\\1721172524-810401.png')
print(image.shape)

cv2.imshow('img', image)




# # CLAHE (Contrast Limited Adaptive Histogram Equalization)
# clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8,8))

# lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
# l, a, b = cv2.split(lab)  # split on 3 different channels

# l2 = clahe.apply(l)  # apply CLAHE to the L-channel

# lab = cv2.merge((l2,a,b))  # merge channels
# img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
# cv2.imshow('Increased contrast', img2)
# #cv2.imwrite('sunset_modified.jpg', img2)

# cv2.waitKey(0)
# cv2.destroyAllWindows()


edges = cv2.Canny(image,100,200)
print(edges.shape)

edges = cv2.resize(edges, (200,115))

cv2.imshow('edges', edges)
cv2.waitKey(0)





# result = image.copy()
# image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# lower = np.array([155,25,0])  
# upper = np.array([179,255,255])
# mask = cv2.inRange(image, lower, upper)
# result = cv2.bitwise_and(result, result, mask=mask)

# cv2.imshow('mask', mask)
# cv2.imshow('result', result)
# cv2.waitKey(0)