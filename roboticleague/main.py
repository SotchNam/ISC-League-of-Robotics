from colorDetection.colorprint import scanColor
from lineDetection.using_cv_demo1 import line_follow, no_line
from crossing import distance
from cameraInput import camera

from threading import Thread
from time import sleep 

import RPI.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#init threads
cameraThread = camera()
colorThread = scanColor()
lineThread = line_follow()
distanceThread = distance()

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
IO.setup(motorsleft, IO.OUT)#motors left
IO.setup(motorsright, IO.OUT)#motors right

def forward():
    .output(motorsleft, True)
    GPIO.output(motorsright, True)

def stop(stoptime):
    GPIO.output(motorsleft, False)
    GPIO.output(motorsright, False)
    time.sleep(stoptime)
    line_follow()

#ig we will have this function control the car
def maiin():
    color = colorThread.color
    dist = distanceThread.dist
    no_line = lineThread.no_line
    cx = lineThread.cx

    if dist < 5:
        GPIO.output(motorsleft, False)
        GPIO.output(motorsright, False)

    if colour == R or colour == G:
        stop(5000)

    if colour == B:
        stop(2000)

    if no_line != True:
        if cx >= 120:
            GPIO.output("P8_10", GPIO.HIGH)
            GPIO.output("P9_11", GPIO.LOW)
        if cx < 120 and cx > 50:
            GPIO.output("P8_10", GPIO.LOW)
            GPIO.output("P9_11", GPIO.LOW)
        if cx <= 50:
            GPIO.output("P8_10", GPIO.LOW)
            GPIO.output("P9_11", GPIO.HIGH)

    else:
        forward()
        time.sleep(1000)#enough time for line cut 15cm dist
        line_follow()



    #print(f"distance={dist}")
    #print(f"color={colorThread.color}")
    #print(cameraThread.frame)
    #print(f"frame={cameraThread.frame}")
    #print(f"line={line}")


if __name__ == '__main__':
    distanceThread.start()
    cameraThread.start()
    colorThread.start()
    lineThread.start()

    while (True):
        maiin()
        colorThread.frame = cameraThread.frame 
        lineThread.frame = cameraThread.frame
        dist = distanceThread.dist
        sleep(2)

"""
for when task is done

colorThread.stop()
lineThread.stop()
distanceThread.stop()
cameraThread.stop()

"""
