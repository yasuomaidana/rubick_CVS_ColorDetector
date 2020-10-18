import numpy as np
import cv2 as cv2


trName= "Track bars HSV format"


#Created to use Trackbar
def nothing(x):
    pass
#Calibration calls bars values
def cali():
    # Obtain HSV values to create mask
    l_h = cv2.getTrackbarPos("Low-H",trName)
    l_s = cv2.getTrackbarPos("Low-S",trName)
    l_v = cv2.getTrackbarPos("Low-V",trName)
    u_h = cv2.getTrackbarPos("High-H",trName)
    u_s = cv2.getTrackbarPos("High-S",trName)
    u_v = cv2.getTrackbarPos("High-V",trName)

    # Create levels arrays
    l_color = np.array([l_h,l_s,l_v])
    u_color = np.array([u_h,u_s,u_v])
    return [l_color, u_color]
#Creates bars to obtain HSV values
def creatBar():
    #### Create track bars
    
    cv2.namedWindow(trName)
    ## Low HSV level
    cv2.createTrackbar("Low-H",trName,0,180,nothing)
    cv2.createTrackbar("Low-S",trName,0,255,nothing)
    cv2.createTrackbar("Low-V",trName,0,255,nothing)
    ## High HSV level
    cv2.createTrackbar("High-H",trName,180,180,nothing)
    cv2.createTrackbar("High-S",trName,255,255,nothing)
    cv2.createTrackbar("High-V",trName,255,255,nothing)
    ### Create track bars end
#Returns mask if user don't want to calibrate
def noCali():
    l_h = 58
    l_s = 201
    l_v = 133
    u_h = 70
    u_s = 248
    u_v = 160

    l_color = np.array([l_h,l_s,l_v])
    u_color = np.array([u_h,u_s,u_v])

    return [l_color, u_color]
# Open the device at the ID 0 
cap = cv2.VideoCapture(1)

cal = int(input("Do you want to calibrate? Yes 1, No 0 : "))
if cal:
    creatBar()

#Check whether user selected camera is opened successfully.
if not (cap.isOpened()):
    print("Could not open video device")
    

while(True): 
    # Capture frame-by-frame
    ret, frame = cap.read()

    #Convert mask to HSV format
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if cal:
        [l_color, u_color] = cali()
    else:
        [l_color, u_color] = noCali()

    #Create mask 
    mask = cv2.inRange(hsv,l_color,u_color)

    #Apply mask to image
    masked = cv2.bitwise_and(hsv,hsv, mask=mask)

    masked = cv2.cvtColor(masked, cv2.COLOR_HSV2BGR)
    # Display the resulting frame
    cv2.imshow('Frame',frame)
    cv2.imshow('Mask',mask)
    cv2.imshow('Masked',masked)
    #Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

## Obtained from calibration

