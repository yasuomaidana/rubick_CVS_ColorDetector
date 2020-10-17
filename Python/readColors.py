import numpy as np
import cv2 as cv2


# Open the device at the ID 0 
cap = cv2.VideoCapture(1)

#Check whether user selected camera is opened successfully.

if not (cap.isOpened()):
    print("Could not open video device")

while(True): 
# Capture frame-by-frame
    ret, frame = cap.read()
# Display the resulting frame
    cv2.imshow('preview',frame)

#Waits for a user input to quit the application

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break