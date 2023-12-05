#importing libs and modules
from colorDetection.colorprint import scanColor
#from lineDetection.using_cv_demo1 import line_follow
from lineFollower import line_follow
from crossing import distance
from cameraInput import camera

import cv2
from threading import Thread, enumerate, main_thread
from time import sleep 

import RPi.GPIO as GPIO
import Falcon
GPIO.setmode(GPIO.BCM)



#init threads
cameraThread = camera()
colorThread = scanColor()
lineThread = line_follow()
distanceThread = distance()

#-------#Setup Pinouts-------#
max_speed= 70 # from 100
min_speed= 64

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
imageWidth = lineThread.frame.shape[1] # = 320
leftMostBound= imageWidth*0.3
leftBound = imageWidth*0.4
center = imageWidth / 2 # 80
rightBound = imageWidth*0.6
rightMostBound= imageWidth*0.7

#control the car
def maiin():

    if dist < 5: #ultrasonic stop
        Falcon.Stop()
        print("stopped")
        print(dist)

    elif colour == G:
        Falcon.Stop()
        sleep(5)
        Falcon.Forward(max_speed)
        sleep(1) # time to skip the color

    elif colour == R:
        Falcon.Stop()
        Falcon.openDoor()
        sleep(5)
        Falcon.Forward(max_speed)
        Falcon.closeDoor()
        sleep(1) # time to skip the color

    elif colour == B:
        Falcon.Stop()
        sleep(2)
        Falcon.Forward(max_speed)
        sleep(1) # time to skip the color

    elif no_line == False:
        if cx < leftMostBound:
            Falcon.TurnLeft(0,max_speed)
            print("left more")
        elif cx <= leftBound and cx >= leftMostBound:
            Falcon.Forward(max_speed,min_speed) # forward(min,max)
            print("left")
        elif cx <= rightBound and cx >= leftBound:
            Falcon.Forward(max_speed)
            print("forward")
        elif cx >= rightBound and cx <= rightMostBound:
            Falcon.Forward(min_speed,max_speed) # forward(min,max)
            print("right")
        elif cx >= rightMostBound:
            Falcon.TurnRight(max_speed,0)
            print("right more")
    else:
        #Falcon.Forward(max_speed)
        print("no line")
        #Falcon.Stop() # continue previous action
        sleep(2) # enough time for line cut 15cm dist

if __name__ == '__main__':
    print("Falcon is ON")
    #Falcon.SpeakBegin()
    #Falcon.FrontLight()

    cameraThread.start()
    print("here we go")
    #time for camera to recieve frames
    sleep(3)
    colorThread.frame = cameraThread.frame 
    lineThread.frame = cameraThread.frame
    distanceThread.start()
    colorThread.start()
    lineThread.start()
    print("started")

    running=True

    while (running):
        try:
            #transfer values between threads
            colorThread.frame = cameraThread.frame 
            lineThread.frame = cameraThread.frame
            color = colorThread.color
            no_line = lineThread.no_line
            cx = lineThread.cx
            dist = distanceThread.dist

            maiin()
            #print(cameraThread.frame)
            #show camera view if needed
            cv2.imshow("test",cameraThread.frame)
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break
            if lineThread.circle:
                #running = False
                print("found circle")

        except KeyboardInterrupt:
            break

    #ending program
    cv2.destroyAllWindows()
    #stop()

    #closing threads
    colorThread.stop()
    lineThread.stop()
    distanceThread.stop()
    cameraThread.stop()
    print("done")

    #time to stop threads
    sleep(0.5)

    #check for still running threads and stop them
    for thread in enumerate():
        try: 
            thread.stop()
        #threads that wont stop
        except AttributeError:
            if thread != main_thread():
                print(thread.name)
