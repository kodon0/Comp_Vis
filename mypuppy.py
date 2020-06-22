import cv2
img = cv2.imread('/Users/kieranodonnell/Desktop/Udemy/Computer-Vision-with-Python/DATA/00-puppy.jpg')

while True:
    cv2.imshow('Pupper', img)

    #If we've waited at least 1ms AND we've pressed Esc, break out
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
