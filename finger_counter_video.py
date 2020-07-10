#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 10:05:36 2020

@author: kieranodonnell
"""


# Imports

import cv2
import numpy as np
from sklearn.metrics import pairwise

# Variable defintion

background = None

accumulated_weight = 0.5

# ROI

roi_top = 20
roi_bottom = 300
roi_right = 300
roi_left = 600

# Calculating accumulated weighted means

def calculate_accum_mean(frame, accumulated_weight):
    
    global background
    
    if background is None:
        background = frame.copy().astype('float')
        return None
    
    cv2.accumulateWeighted(frame, background, accumulated_weight)
    
# Use thresholding to get hand from ROI

def segment(frame,threshold_min = 30):
    
    diff = cv2.absdiff(background.astype('uint8'), frame)
    
    ret,thresholded = cv2.threshold(diff,threshold_min,255, cv2.THRESH_BINARY)
    
    contours, hierarchy = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    
    if len(contours) == 0: # Check if contour was acquired
        return None
    else:
        # Assuming largest contour in ROI is a hand
        hand_segment = max(contours,key=cv2.contourArea)
        
        return (thresholded, hand_segment)
    
# Using convex hull polygon with hand input
# Calculate most extreme points, then use their intersect to estimate hand center
# Calculate distance from centroid to furtherest point
# Draw circle at centroid -> any points outside shoudl be extended fingers!

def finger_counter(thresholded, hand_segment):
    
    # Grabbing extreme points
    convex_hull = cv2.convexHull(hand_segment)
    top    = tuple(convex_hull[convex_hull[:, :, 1].argmin()][0])
    bottom = tuple(convex_hull[convex_hull[:, :, 1].argmax()][0])
    left   = tuple(convex_hull[convex_hull[:, :, 0].argmin()][0])
    right  = tuple(convex_hull[convex_hull[:, :, 0].argmax()][0])
    
    c_x = (left[0] + right[0])// 2 
    c_y = (top[1] + bottom[1])// 2
    
    distance = pairwise.euclidean_distances([(c_x, c_y)], Y=[left,right,top,bottom])[0]
    max_distance = distance.max()
    
    # Make a circle 90% of max distance -> can be changed
    rad = int(0.9 * max_distance)
    circum = (2*np.pi*rad)
    
    # Make circle ROI
    circle_roi = np.zeros(thresholded.shape[:2],dtype='uint8')
    cv2.circle(circle_roi,(c_y,c_x),rad,255,10)

    circle_roi = cv2.bitwise_and(thresholded,thresholded, mask = circle_roi)    
    
    contours, hierarchy = cv2.findContours(circle_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]
    
    count = 0
    
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        out_wrist_pos = (c_y + (c_y*0.25)) > (y+h)
        point_limits = ((circum*0.25) > contour.shape[0])
        
        if out_wrist_pos and point_limits:
            count += 1
            
    return count
    
 # Unification
 
cam = cv2.VideoCapture(0)
 
nb_frames = 0
 
while True:
    ret, frame = cam.read()
    frame_copy = frame.copy()
     
    roi = frame[roi_top:roi_bottom, roi_right:roi_left]
     
    gray_scale = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
     
    gray_scale = cv2.GaussianBlur(gray_scale,(5,5),0)
     
    if nb_frames < 60:
        calculate_accum_mean(gray_scale, accumulated_weight)
         
        if nb_frames <= 59:
            cv2.putText(frame_copy,'Please wait, Gathering Background', (200,300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255),2)
            cv2.imshow('Finger count', frame_copy)
    else:
         hand = segment(gray_scale)
            
         if hand is not None:
             thresholded, hand_segment = hand
                
             # Draw contour around hand in livestream
             cv2.drawContours(frame_copy, [hand_segment + (roi_right, roi_top)], -1, (255, 0 , 255),7)
             
             # Count the fingers   
             fingers = finger_counter(thresholded, hand_segment)
             
             # Display count    
             cv2.putText(frame_copy, str(fingers), (70,45),  cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),2)
              
             # Display the thresholded image 
             cv2.imshow('Threshold', thresholded)
    
                
    cv2.rectangle(frame_copy,(roi_left,roi_top), (roi_right,roi_bottom), (0,255,0), 5)
         
    nb_frames += 1
         
    cv2.imshow('Finger count', frame_copy)
         
    k = cv2.waitKey(1) & 0xFF
         
    if k == 27:
        break
cam.release()
cv2.destroyAllWindows