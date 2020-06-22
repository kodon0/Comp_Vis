import cv2
import numpy as np
# Create a function based on a CV2 Event (Left button click)

# mouse callback function - almost the same as drawing on pics
def draw_rectangle(event,x,y,flags,param):

    global pt1,pt2,topLeft_clicked,botRight_clicked

    # get mouse click
    if event == cv2.EVENT_LBUTTONDOWN:

        if topLeft_clicked == True and botRight_clicked == True:
            topLeft_clicked = False
            botRight_clicked = False
            pt1 = (0,0)
            pt2 = (0,0)

        if topLeft_clicked == False:
            pt1 = (x,y)
            topLeft_clicked = True

        elif botRight_clicked == False:
            pt2 = (x,y)
            botRight_clicked = True

# Rectangle definition -> top left and bottom right points
pt1 = (0,0)
pt2 = (0,0)
topLeft_clicked = False
botRight_clicked = False

cap = cv2.VideoCapture(0)

# Create a named window for connections
cv2.namedWindow('Video Window')

# Bind draw_rectangle function to mouse cliks
cv2.setMouseCallback('Video Window', draw_rectangle)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if topLeft_clicked == True:
        #Circle is initial marker
        cv2.circle(frame, center=pt1, radius=5, color=(255,0,0), thickness=2)

    #drawing rectangle
    if topLeft_clicked and botRight_clicked:
        cv2.circle(frame, center=pt2, radius=5, color=(255,0,0), thickness=2)
        cv2.rectangle(frame, pt1, pt2, (0, 0, 255), 10)


    # Display the resulting frame
    cv2.imshow('Video Window', frame)

    # This command let's us quit with the "q" button on a keyboard.
    # Simply pressing X on the window won't work!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
