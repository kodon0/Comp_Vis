#This script activates the webcam
#This means YOUR webcam (if you're reading this)
#Check it!
import cv2


# Connects to your computer's default camera
cap = cv2.VideoCapture(0)


# Automatically grab width and height from video feed
# (returns float which we need to convert to integer for later on!)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Saving to files -> MacOs = XVID
writer = cv2.VideoWriter('mycapturevid.mp4', cv2.VideoWriter_fourcc(*'XVID'),30, (width, height))

while True:

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    writer.write(frame)

    # Display the resulting frame
    cv2.imshow('frame',frame)

    # This command let's us quit with the "q" button on a keyboard.

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy the windows
cap.release()
writer.release()
cv2.destroyAllWindows()
