import cv2
import numpy as np
import RPi.GPIO as gpio
from matplotlib.pyplot import text
import numpy as np
import Falcon
import imutils
import time

#-------#Setup Pinouts-------#
en1=20
en2=21
in1=17
in2=22
in3=23
in4=24
gpio.setmode(gpio.BCM)
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(in3, gpio.OUT)
gpio.setup(in4, gpio.OUT)
gpio.setup(en1,gpio.OUT)
gpio.setup(en2,gpio.OUT)
#p1 = gpio.PWM(en1, 100)
#p2 = gpio.PWM(en2, 100)
Falcon.Stop()
#----------------------------#

#-------#Setup Camera-------#

cap= cv2.VideoCapture(0)

cap.set(3, 160)
cap.set(4, 120)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 70)
cap.set(cv2.CAP_PROP_SATURATION, 50)
cap.set(cv2.CAP_PROP_CONTRAST, 100)

#------------#LineDetection------------#
max_speed= 70
min_speed= 64

print("FALCON is ON,,")
#Falcon.SpeakBegin()
Falcon.FrontLight()
 
while(True):

    # Capture the frames

    ret, frame = cap.read()

    # Crop the image

    crop_img = frame[60:120, 0:160]


    # Convert to grayscale

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)


    # Gaussian blur

    blur = cv2.GaussianBlur(gray,(5,5),0)

 

    # Color thresholding

    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)


    # Find the contours of the frame

    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)


    # Find the biggest contour (if detected)

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        M = cv2.moments(c)


        cx = int(M['m10']/M['m00'])

        cy = int(M['m01']/M['m00'])

 

        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)

        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

 

        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

 

        if cx >= 120:

            print("Turn Right")
            Falcon.TurnRight(min_speed,max_speed)

 

        if cx < 120 and cx > 50:

            print("On Track!")
            Falcon.Forward(max_speed)

 

        if cx <= 50:

            print("Turn Left")
            Falcon.TurnLeft(min_speed,max_speed)

 

else:
    print ("I don't see the line")
    Falcon.Stop()
    self.no_line = True
#Display the resulting frame

cv2.imshow('frame',crop_img)

if cv2.waitKey(1) & 0xFF == ord('q'):
    Falcon.Stop()
    #break
cap.release()
cv2.destroyAllWindows()
