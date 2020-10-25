#Library used to process data
import numpy as np
#Library used to have acces to camera
import cv2 as cv2
from rubik_solver import utils

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

    #Obtain kernel size
    ks = cv2.getTrackbarPos("KS","Kernel Size")

    return [l_color, u_color,ks]

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

    ##Bar to get kernel
    cv2.namedWindow("Kernel Size")
    cv2.createTrackbar("KS","Kernel Size",0,255,nothing)

#Returns the values to generate mask if user don't want to calibrate
def noCali():
    l_h = 58
    l_s = 201
    l_v = 133
    u_h = 70
    u_s = 248
    u_v = 160

    l_color = np.array([l_h,l_s,l_v])
    u_color = np.array([u_h,u_s,u_v])
    KS = 23

    return [l_color, u_color,KS]

##Configuring OpenCV
# Open the device at the ID 0 
cap = cv2.VideoCapture(1)
font = cv2.FONT_HERSHEY_SIMPLEX

#cal = int(input("Do you want to calibrate? Yes 1, No 0 : "))


#Check whether user selected camera is opened successfully.
if not (cap.isOpened()):
    print("Could not open video device")
    

#Obtains the mask used for obtain the color cells
def Obtain_Mask():
    cal = 0
    if cal:
        creatBar()
    while(True): 
        # Capture frame-by-frame
        _, frame = cap.read()
        #Convert mask to HSV format
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if cal:
            [l_color, u_color,ks] = cali()
        else:
            [l_color, u_color,ks] = noCali()

        #Create mask 
        mask = cv2.inRange(hsv,l_color,u_color)

        #Erode mask
        kernel = np.ones((ks,ks),np.uint8)
        mask = cv2.erode(mask,kernel)
        #Dilatation
        mask = cv2.dilate(mask, kernel)
                
        #Waits for a user input to quit the application
        if cv2.waitKey(1) & 0xFF == ord('w'):
            return mask
        else:
            cv2.putText(mask,"Press W key",(0,100),font,.9,(255,255,255),2) 
            # Display the resulting frame
            cv2.imshow('Mask',mask)
    
#Check wich color is given an array
def checkCol(color):
    verde = np.array([5, 148, 10])
    naranja = np.array([7, 167, 245])
    amarillo = np.array([10,255,251])  
    rojo = np.array([2, 0, 232]) 
    blanco = np.array([254, 254, 254]) 
    azul = np.array([244, 0, 3]) 

    if(np.array_equal(color,verde)):
        return "g"
    if(np.array_equal(color,naranja)):
        return "o"
    if(np.array_equal(color,amarillo)):
        return "y"
    if(np.array_equal(color,rojo)):
        return "r"
    if(np.array_equal(color,blanco)):
        return "w"
    if(np.array_equal(color,azul)):
        return "b"
#Returns an array that indicates which colors are in ona face
def obtainColors(mask):
    while(True):
        # Capture frame-by-frame
        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #Apply mask to image
        masked = cv2.bitwise_and(hsv,hsv, mask=mask)
        #Convert again to BGR format
        masked = cv2.cvtColor(masked, cv2.COLOR_HSV2BGR)
        
        #Obtain regions
        _,contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        na=1
        ret=np.array(["","","","","","","","",""])
        for cnt in contours:
            
            #len(cnt) number of sides 3 triangle...
            #area = cv2.contourArea(cnt) 
            approx = cv2.approxPolyDP(cnt,0.08*cv2.arcLength(cnt,True),True)#approx, list of points of the rectangle
            #print(approx)
            #Obtain points of approx to put text
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            #Obtains the moments
            mom = cv2.moments(cnt)
            #Obtains the center using moments
            cen = (int(mom['m10'] / (mom['m00'] + 1e-5)), int(mom['m01'] / (mom['m00'] + 1e-5))) #mx,my
            
            cv2.drawContours(frame,[approx],0,(0,0,0),5)
            #Write name of the contour
            
            
            color = frame[cen[1]][cen[0]]
            ret[9-na]=checkCol(color)
            cv2.putText(frame,ret[9-na]+str(9-(na-1)),(x+20,y+40),font,.5,(0,0,0),2)

            na+=1
        #ret=ret[:-1]
        cv2.putText(frame,"Press W key",(150,100),font,.5,(0,0,0),2)
        # Display the resulting frame
        cv2.imshow('Frame',frame)
        
        #Waits for a user input to quit the application
        if cv2.waitKey(1) & 0xFF == ord('w'):
            return ret

#Generates a black image with a message
def message(mss):
    blackscreen = np.zeros((480,640))
    while(True):
        cv2.putText(blackscreen,mss+" then press Q key",(0,100),font,.5,(254,254,254),2)
        cv2.imshow('Message',blackscreen)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
#Inicialices faces
faces=[]

message("Reset the cube")
cv2.destroyAllWindows()
mask = Obtain_Mask()
cv2.destroyAllWindows()

message("Scramble the cube and select Yellow as front and Orange as top")
cv2.destroyAllWindows()
faces.append(obtainColors(mask))

message("Select Blue as front face and Yellow as top face")
cv2.destroyAllWindows()
faces.append(obtainColors(mask))

message("Select Red as front face")
cv2.destroyAllWindows()
faces.append(obtainColors(mask))

message("Select Green as front face")
cv2.destroyAllWindows()
faces.append(obtainColors(mask))

message("Select Orange as front face")
cv2.destroyAllWindows()
faces.append(obtainColors(mask))

message("Select White as front face and Red as top face")
cv2.destroyAllWindows()
faces.append(obtainColors(mask))

message("Select Green as front face and White as top face")
cv2.destroyAllWindows()

cap.release()
send=''
for i in faces:
    for j in i:
        send+=j
    print(i)

print(send)
solution = utils.solve(send, 'Kociemba')
#from rubik.cube import Cube not used 
#print(Cube(send))

#Libraries used to acces to comunication
import socket
import array as arr

# Dictionary of cube moves
movesDict = {
	"D":	0,
	"D2": 	1,
	"D'": 	2,
	"L": 	3,
	"L2": 	4,
	"L'": 	5,
	"F": 	6,
	"F2": 	7,
	"F'": 	8,
	"R": 	9,
	"R2": 	10,
	"R'": 	11,
	"B": 	12,
	"B2":	13,
	"B'":	14,
	"U": 	15,
	"U2":	16,
	"U'":	17
}
#Obtain the number of moves
nMoves = len(solution)
command = 0xFB
payloadLen = nMoves
#Start the format message
packet = arr.array('B', [0] * (payloadLen + 2))
packet[0] = command
packet[1] = payloadLen
print(solution)
#for idx in range(0, nMoves):
solution2=[]
for i in solution:
    solution2.append(str(i))
print(solution2)
for idx in range(0, nMoves):
    packet[idx + 2] = movesDict[solution2[idx]]

# Connect TCP/IP client to localhost in port 2500
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 2500))

# Write packet to cube simulator
client.send(packet)
client.close()