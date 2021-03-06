# https://stackoverflow.com/questions/69961871/how-to-compute-mean-and-standard-deviation-of-edges-canny-edge-detection-in-ope
# https://answers.opencv.org/question/119161/detecting-not-decoding-datamatrix-rectangle-regions-in-an-image/
# http://note.sonots.com/SciSoftware/haartraining.html
#https://stackoverflow.com/questions/29365813/opencv-2d-barcode-data-matrix-detection
#https://github.com/egonSchiele/OpenCV/blob/master/samples/python/squares.py

import cv2
from cv2 import CV_32SC2
from cv2 import CV_32S
import numpy as np
from utils import image_resize




#image = cv2.imread(r"/home/dntx/win/reps/DataMatrix-Sorter/app/IMG_20220330_0757191_50p.jpg")
#image = cv2.imread(r"/home/dntx/win/reps/DataMatrix-Sorter/app/l1.jpg")
#image = cv2.imread(r"/home/dntx/win/reps/DataMatrix-Sorter/app/l2.jpg")
image = cv2.imread(r"/home/dntx/win/reps/DataMatrix-Sorter/app/l3.jpg")

image = image_resize(image, height=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#blur = cv2.medianBlur(gray, 5)

mean, std = cv2.meanStdDev(gray)
x = 1.4
tr_1 = mean - x*std
tr_2 = mean + x*std

thresh = cv2.inRange(gray, tr_1, tr_2)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# calculate min area of data matrix
full_area = image.shape[0] * image.shape[1]
dm_area = full_area / 200

# get boundle rectanles
for c in contours: 
        area = cv2.contourArea(c)
        if area > dm_area and area < full_area - 1000:
                cv2.drawContours(image, [c], 0, (0,0,255), 2)
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 1)

# get masks according to rectangles

# check histogramms for this areas

# if histogramm is similar for datamatrix, return this part of image




cv2.imshow('thresh', thresh)
cv2.imshow('hsv', image)
cv2.waitKey()




# harris = cv2.cornerHarris(gray, 2, 5, 0.04) 

# _, thr = cv2.threshold(harris, 0.001 * harris.max(), 255, cv2.THRESH_BINARY)
# thr = thr.astype('uint8')

# contours, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# contours = list(filter(lambda x: cv2.contourArea(cv2.convexHull(x)) > 1000, contours))

# #print(contours)

# for i, contour in enumerate(contours):
#         mask = np.zeros_like(image)
#         cv2.drawContours(gray, contour, -1, (255, 0, 0), -1)








# blur = cv2.medianBlur(gray, 5)


# mean, std = cv2.meanStdDev(blur)

# #print(mean, std)

# x = 1.7

# tr_1 = mean - x*std
# tr_2 = mean + x*std


# # threshold on background color
# thresh = cv2.inRange(blur, tr_1, tr_2)

# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
# close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# blur = cv2.blur(close, (3, 3))




# edges = cv2.Canny(blur,100,200)


# cv2.imshow('thresh', edges)
# cv2.waitKey()





# cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]


#print(cnts)

# min_area = 100
# max_area = 2500
# image_number = 0
# for c in cnts:
#     area = cv2.contourArea(c)
#     #print(area)
#     #if area > min_area and area < max_area:
#     x,y,w,h = cv2.boundingRect(c)
#         # ROI = image[y:y+h, x:x+w]
#         # cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
#     cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
#     image_number += 1




# sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
# sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

# thresh = cv2.threshold(sharpen,220,255, cv2.THRESH_BINARY_INV)[1]
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
# close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)


# mser = cv2.MSER_create()
# mser.setMinArea(50)
# mser.setMaxArea(100)
# regions, _ = mser.detectRegions(close)

# hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
# cv2.polylines(image, hulls, 1, (0, 0, 255), 2)




# cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# print(cnts)

# min_area = 100
# max_area = 2500
# image_number = 0
# for c in cnts:
#     area = cv2.contourArea(c)
#     print(area)
#     if area > min_area and area < max_area:
#         x,y,w,h = cv2.boundingRect(c)
#         # ROI = image[y:y+h, x:x+w]
#         # cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
#         cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
        # image_number += 1

# cv2.imshow('gray', gray)
# cv2.imshow('blur', blur)
# cv2.imshow('sharpen', sharpen)
# cv2.imshow('thresh', edges)
# cv2.waitKey()
