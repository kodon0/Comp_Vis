#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 12:26:30 2020

@author: kieranodonnell
"""


# Watershed Algorithm with custom seeds
# Run this script with any imported image.
# The algorithm will take in user clicks for segmentation of an Image
# Use number keys on keyboard to choose layers/background/foreground
# Good for object detection!

import cv2
import numpy as np
import matplotlib.pyplot as plt


pic = cv2.imread('GitHub/Comp Vis/dataset/training_set/dogs/dog.16.jpg')
pic_copy = np.copy(pic)

# plt.imshow(pic)

marker_image = np.zeros(pic.shape[:2],dtype=np.int32)
segments = np.zeros(pic.shape,dtype=np.uint8)

#https://matplotlib.org/examples/color/colormaps_reference.html color mapping in plt
# Will use set3 in this case

from matplotlib import cm
cm.tab10(0)

def make_rgb(i):

    return tuple(np.array(cm.tab10(i)[:3])*255)

colors = []
for i in range(10):
        colors.append(make_rgb(i))

### Global Vars
# Color choice
current_marker = 1
n_markers = 10 # 0->9
# Updated marker by watershed
marks_updated = False

# Callback

def mouse_callback(event,x,y,flags,param):
    global marks_updated

    if event == cv2.EVENT_LBUTTONDOWN:
        # Markers passed to watershed
        cv2.circle(marker_image, (x,y), 5, (current_marker), -1)

        # Seeing image
        cv2.circle(pic_copy, (x,y), 5, colors[current_marker], -1)

        marks_updated = True

# While true
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', mouse_callback)

while True:

    # SHow the 2 windows
    cv2.imshow('WaterShed Segments', segments)
    cv2.imshow('Image', pic_copy)


    # Close everything if Esc is pressed
    k = cv2.waitKey(1)

    if k == 27:
        break

    # Clear all colors and start over if 'c' is pressed
    elif k == ord('c'):
        _copy = pic.copy()
        marker_image = np.zeros(pic.shape[0:2], dtype=np.int32)
        segments = np.zeros(pic.shape,dtype=np.uint8)

    # If a number 0-9 is chosen index the color
    elif k > 0 and chr(k).isdigit():
        # chr converts to printable digit

        current_marker  = int(chr(k))

        # CODE TO CHECK INCASE USER IS CARELESS
#         n = int(chr(k))
#         if 1 <= n <= n_markers:
#             current_marker = n

    # If we clicked somewhere, call the watershed algorithm on our chosen markers
    if marks_updated:

        marker_image_copy = marker_image.copy()
        cv2.watershed(pic, marker_image_copy)

        segments = np.zeros(pic.shape,dtype=np.uint8)

        for color_ind in range(n_markers):
            segments[marker_image_copy == (color_ind)] = colors[color_ind]

        marks_updated = False

cv2.destroyAllWindows()
