#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 14:36:53 2020

@author: kieranodonnell
"""


# Camshift Tracking with default frontal haar cascade
# Needs a face to detect!


import numpy as np
import cv2

cap = cv2.VideoCapture(0)
ret,frame = cap.read()

# Using a face cascade
face_cascade = cv2.CascadeClassifier('/Users/kieranodonnell/Documents/GitHub/Comp Vis/haarcascades/haarcascade_frontalface_default.xml')

# Draw rectangle around face
face_rects = face_cascade.detectMultiScale(frame)

(face_x,face_y,w,h) = tuple(face_rects[0])
tracking_window = (face_x,face_y,w,h)

# Making ROI for tracking
roi = frame[face_y:face_y+h, face_x:face_y+w]

# Using HSV inROI
hsv_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

# Use color histogram to backproject
roi_hist = cv2.calcHist([hsv_roi],[0],None,[180],[0,180])

# Normalise historgam array
cv2.normalize(roi_hist,roi_hist, 0, 255, cv2.NORM_MINMAX)

term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10,1)

# Loop

while True:
    
    ret,frame = cap.read()
    
    if ret == True:
        
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0,180],1)
        
        # Activate below for meanshift instead of camshift
        
        '''ret,tracking_window = cv2.meanShift(dst,tracking_window, term_criteria)
        
        x,y,w,h = tracking_window
        
        img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),1)'''
        
        ret, tracking_window = cv2.CamShift(dst,tracking_window,term_criteria)
        
        points = cv2.boxPoints(ret)
        
        points = np.int0(points)
        
        img2 = cv2.polylines(frame,[points],True,(0,255,255),2)
        
        cv2.imshow('Image',img2)
        
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    else:
        break
cv2.destroyAllWindows()
cap.release