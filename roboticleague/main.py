#importing libs and modules
from colorDetection.colorprint import scanColor
#from lineDetection.using_cv_demo1 import line_follow
from lineFollower import line_follow
#from crossing import distance
from cameraInput import camera

import cv2
from threading import Thread, enumerate, main_thread
from time import sleep 
#import RPI.GPIO as GPIO


"""
#init gpio
#GPIO.setmode(GPIO.BCM)
# Setup Output Pins
# Left Forward
GPIO.setup("P8_10", GPIO.OUT)
# Right Forward
GPIO.setup("P9_11", GPIO.OUT)

# start the motors
GPIO.output("P8_10", GPIO.HIGH)
GPIO.output("P9_11", GPIO.HIGH)
motorsleft=1
motorsright=2
#IO.setup(motorsleft, IO.OUT)#motors left
#IO.setup(motorsright, IO.OUT)#motors right
"""

#init threads
cameraThread = camera()
colorThread = scanColor()
lineThread = line_follow()
#distanceThread = distance()

"""
def forward():
    GPIO.output(motorsleft, True)
    GPIO.output(motorsright, True)

def stop():
    GPIO.output(motorsleft, False)
    GPIO.output(motorsright, False)

def left():
    GPIO.output(motorsleft, False)
    GPIO.output(motorsright, True)

def right():
    GPIO.output(motorsleft, True)
    GPIO.output(motorsright, False)
"""

#control the car
def maiin():

    """
    if dist < 5: #ultrasonic stop
        stop()
        print("stopped")

    elif colour == R or colour == G:
        stop()
        sleep(5)

    elif colour == B:
        stop()
        sleep(2)

    elif no_line = False:
        if cx >= 120:
            right()?
            GPIO.output("P8_10", GPIO.HIGH)
            GPIO.output("P9_11", GPIO.LOW)
        if cx < 120 and cx > 50:
            forward()?
            GPIO.output("P8_10", GPIO.LOW)
            GPIO.output("P9_11", GPIO.LOW)
        if cx <= 50:
            left()?
            GPIO.output("P8_10", GPIO.LOW)
            GPIO.output("P9_11", GPIO.HIGH)
    else:
        forward()
        sleep(10)#enough time for line cut 15cm dist

    """

if __name__ == '__main__':
    cameraThread.start()
    #time for camera to recieve frames
    sleep(3)
    #distanceThread.start()
    colorThread.frame = cameraThread.frame 
    lineThread.frame = cameraThread.frame
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
            #dist = distanceThread.dist

            maiin()
            #print(lineThread.frame)
            #show camera view if needed
            cv2.imshow("test",cameraThread.frame)
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break
            if lineThread.circle:
                running = False
                print("found circle")

        except KeyboardInterrupt:
            break

    #ending program
    cv2.destroyAllWindows()
    #stop()

    #closing threads
    colorThread.stop()
    lineThread.stop()
    #distanceThread.stop()
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
