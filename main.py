#importing libs and modules
import time
from colorDetection.colorprint import scanColor
#from lineDetection.using_cv_demo1 import line_follow
from lineFollower import line_follow
from crossing import distance
from cameraInput import camera

import cv2
from threading import Thread, enumerate, main_thread
from time import sleep 

import RPi.GPIO as gpio
import Falcon
gpio.setmode(gpio.BCM)



#init threads
cameraThread = camera()
colorThread = scanColor()
lineThread = line_follow()
distanceThread = distance()

#-------#Setup Pinouts-------#
max_speed= 48 # from 100
min_speed= 20
min_speed2= 15

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
imageWidth = 160 #lineThread.frame.shape[1] # = 320
leftMostBound= imageWidth*0.255
leftBound = imageWidth*0.45
center = imageWidth / 2 # 80
rightBound = imageWidth*0.55
rightMostBound= imageWidth*0.705

def forwardTimed(speed1,speed2,timerd):
            duration = timerd
            start_time = time.time()
            while time.time() - start_time < duration:
                Falcon.Forward(speed1,speed2) 

#control the car

isStuck = False
def maiin():

    global isStuck
    #if dist < 5: #ultrasonic stop
        #Falcon.Stop()
        #print("stopped")
        #print(dist)
    #print(cx)
    try:
        #elif color == 'G':
        if color == 'G':
            forwardTimed(max_speed,max_speed,0.3)
            forwardTimed(0,0,5)
            forwardTimed(max_speed,max_speed,0.3)

        elif color == 'R':
            forwardTimed(max_speed,max_speed,0.3)
            Falcon.openDoor()
            forwardTimed(0,0,5)
            Falcon.closeDoor()
            forwardTimed(max_speed,max_speed,0.3)

        elif color == 'B':
            forwardTimed(max_speed,max_speed,0.3)
            forwardTimed(0,0,2)
            forwardTimed(max_speed,max_speed,0.3)

        elif cx == None:
            forwardTimed(min_speed2,max_speed,0.1)

        elif no_line == False or isStuck:
            if no_line == False:
                isStuck = False
            if cx < leftMostBound:
                #Falcon.Forward(0,max_speed+20)
                forwardTimed(min_speed2,max_speed,0.3)
                print("left more")
            elif cx <= leftBound and cx >= leftMostBound:
                #Falcon.Forward(max_speed,min_speed) # forward(min,max)
                forwardTimed(min_speed,max_speed,0.05)
                print("left")
            elif cx <= rightBound and cx >= leftBound:
                Falcon.Forward(max_speed)
                print("forward")
            elif cx >= rightBound and cx <= rightMostBound:
                #Falcon.Forward(min_speed,max_speed) # forward(min,max)
                forwardTimed(max_speed,min_speed,0.05)
                print("right")
            elif cx >= rightMostBound:
                #Falcon.Forward(max_speed+20,0)
                forwardTimed(max_speed,min_speed2,0.3)
                print("right more")
            #time.sleep(0.05)

        else:
            forwardTimed(min_speed,min_speed,0.2)
            #Falcon.Forward(max_speed)
            print("no line")
            isStuck = True
            #Falcon.Stop() # continue previous action
            #sleep(2) # enough time for line cut 15cm dist
    except TypeError:
        pass

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
    #distanceThread.start()
    colorThread.start()
    lineThread.start()
    print("started")

    running=True

    while (running):
        try:
            #transfer values between threads
            colorThread.frame = cameraThread.frame 
            lineThread.frame = cameraThread.frame
            print(lineThread.cx)
            color = colorThread.color
            no_line = lineThread.no_line
            cx = lineThread.cx
            dist = distanceThread.dist

            #forwardTimed(max_speed,max_speed,1)
            #forwardTimed(0,0,1)
            maiin()
            #print(cameraThread.frame)
            #show camera view if needed
            #cv2.imshow("test",cameraThread.frame)
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break
            if lineThread.circle:
                running = False
                print("found circle")

        except KeyboardInterrupt:
            running = False
            break

    #ending program
    cv2.destroyAllWindows()
    #stop()

    #closing threads
    colorThread.stop()
    lineThread.stop()
    #distanceThread.stop()
    cameraThread.stop()
    gpio.cleanup()
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
