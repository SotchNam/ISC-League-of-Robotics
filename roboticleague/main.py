import RPI.GPIO as GPIO
import time
#from /color_detectiion/colorprint/ import scanColor
#from /line detection/using_cv_demo1/ import line_follow, no_line
from crossing import distance
GPIO.setmode(GPIO.BCM)

motorsleft=1
motorsright=2
IO.setup(motorsleft, IO.OUT)#motors left
IO.setup(motorsright, IO.OUT)#motors right

def forward():
    GPIO.output(motorsleft, True)
    GPIO.output(motorsright, True)

def stop(stoptime):
    GPIO.output(motorsleft, False)
    GPIO.output(motorsright, False)
    time.sleep(stoptime)
    line_follow()

def maiin():

    ######################################needs threading here#################################
    line_follow()
    colour = scanColor()
    dist = distance()

    if dist < 5:
        GPIO.output(motorsleft, False)
        GPIO.output(motorsright, False)

    if colour == R or colour == G:
        stop(5000)

    if colour == B:
        stop(2000)

    if no_line == True:
        forward()
        time.sleep(1000)#enough time for line cut 15cm dist
        line_follow()


while True:
    if __name__ == '__main__':
        webcam = cv2.VideoCapture(0)
        while (True):
            maiin()