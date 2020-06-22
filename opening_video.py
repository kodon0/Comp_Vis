import cv2
import time #So video plays in a normal speed -> i.e frame = recorded framerate

cap = cv2.VideoCapture('mycapturevid.mp4')

# Fps of read in video
fps = 30

# Check if the video was acutally there

if cap.isOpened()== False:
    print("Error opening the video file. Please double check your file path for typos. Or move the movie file to the same location as this script/notebook")


# While the video is opened
while cap.isOpened():



    # Read the video file.
    ret, frame = cap.read()

    # If we got frames, show them.
    if ret == True:




         # Display the frame at same frame rate of recording
        # Watch lecture video for full explanation
        time.sleep(1/fps)
        cv2.imshow('frame',frame)

        # Press q to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):

            break

    # Or automatically break this whole loop if the video is over.
    else:
        break

cap.release()
# Closes all the frames
cv2.destroyAllWindows()
