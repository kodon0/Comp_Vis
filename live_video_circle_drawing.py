#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:55:33 2020

@author: kieranodonnell
"""


#Drawing Red Circle on Live Video Script

'''This script draws red circles with right mouse.
It draws a big orange/brown circle and follows the mouse cursor.
Press q to quit'''

import cv2
import numpy as np

drawing = False #True is mose moves



# Mouse callback function -> red circle
def draw_red_circle(event,x,y,flags,param):

    global drawing, pt1

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True


    elif event == cv2.EVENT_MOUSEMOVE:
    #Moving mouse
        if drawing == True:
            #Move point of mouse with circle
            pt1 = (x,y)


    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

pt1 = (0,0)


# Open camera
cap = cv2.VideoCapture(0)
# This names the window so we can reference it
cv2.namedWindow(winname='Live Circles!')
# Connects the mouse button to our callback function
cv2.setMouseCallback('Live Circles!',draw_red_circle)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if drawing == True:
        #Cirlce
        cv2.circle(frame, center=pt1, radius=200, color=(50,100,200), thickness=50)


    # Display the resulting frame
    cv2.imshow('Live Circles!', frame)

    # This command let's us quit with the "q" button on a keyboard.
    # Simply pressing X on the window won't work!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
