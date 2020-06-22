#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 16:19:48 2020

@author: kieranodonnell
"""
 

#Drawing Green Circle Script

'''This script draws green circles with right mouse. Press escape to enter'''

import cv2
import numpy as np


# Mouse callback function -> red circle
def draw_red_circle(event,x,y,flags,param):
    
    
    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(img, (x,y), radius = 25, color = (0,255,0), thickness = 10)
  
        


# Create a black image
img = np.zeros((1024,1024,3), np.uint8)
# This names the window so we can reference it 
cv2.namedWindow(winname='Circles!')
# Connects the mouse button to our callback function
cv2.setMouseCallback('Circles!',draw_red_circle)

while True:
     cv2.imshow('Circles!',img)
     if cv2.waitKey(20) & 0xFF == 27:
        break
    
cv2.destroyAllWindows