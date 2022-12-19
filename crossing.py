# Libraries
import RPi.GPIO as GPIO
import time
from threading import Thread
# set GPIO Pins
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 8
GPIO_ECHO = 25
class distance(Thread):
    def __init__(self):
        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        # set GPIO Pins
        GPIO_TRIGGER = 8
        GPIO_ECHO = 25

        # set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)

        self.dist = 0
        self.on= False
        super().__init__()

    def start(self):
        Thread(target = self.run,args=()).start()
        return self

    def run(self):
        self.on = True
        while self.on:
            #delay to improve threading, removes stress from cpu
            time.sleep(0.1)
            # set Trigger to HIGH
            GPIO.output(GPIO_TRIGGER, True)
            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, False)

            StartTime = time.time()
            StopTime = time.time()

            # save StartTime
            while GPIO.input(GPIO_ECHO) == 0:
                StartTime = time.time()

            # save time of arrival
            while GPIO.input(GPIO_ECHO) == 1:
                StopTime = time.time()

            # time difference between start and arrival
            TimeElapsed = StopTime - StartTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            self.dist= (TimeElapsed * 34300) / 2

        def stop(self):
            self.on = False
            GPIO.cleanup()

if __name__ == '__main__':
     distanceThread = distance()
     distanceThread.start()
     try:
         while True:
             print ("Measured Distance = %.1f cm" % distanceThread.dist)
             time.sleep(1)
#
#         # Reset by pressing CTRL + C
     except KeyboardInterrupt:
         print("Measurement stopped by User")
