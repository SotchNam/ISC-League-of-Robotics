### Import Libraries:
import time
import tinyik
import numpy as np
import RPi.GPIO as gpio
#import pyttsx3 # Text to Speech Library
#engine = pyttsx3.init() # object creation

### Import the PCA9685 module:
import Adafruit_PCA9685
from board import SCL, SDA
import busio
#from adafruit_motor import servo
#from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA) # Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685() # Create a simple PCA9685 class instance.
#pca = PCA9685(i2c)
#pca.frequency = 60

#Servo Channels:
##servo0= servo.Servo(pca.channels[0])
##servo1= servo.Servo(pca.channels[1])
##servo2= servo.Servo(pca.channels[2])
##servo3= servo.Servo(pca.channels[3])
##servo4= servo.Servo(pca.channels[4])
##servo5= servo.Servo(pca.channels[5])

#LED Channels:
##LedF= servo.Servo(pca.channels[8])
##LedR= servo.Servo(pca.channels[9])
##LedL= servo.Servo(pca.channels[10])
##LedB= servo.Servo(pca.channels[11])
#Setting Channels:
##Set0= servo.Servo(pca.channels[13])
##Set90= servo.Servo(pca.channels[14])
##Set180= servo.Servo(pca.channels[15])

###Variables:
#time:
tsll=0.2
tsl=0.7
tsh=1
t1=3
#L298n:
speed=100
en1=20
en2=21
in3=17
in4=22
in1=23
in2=24
#Setting DC Motors Controllers:
gpio.setmode(gpio.BCM)
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(in3, gpio.OUT)
gpio.setup(in4, gpio.OUT)
gpio.setup(en1,gpio.OUT)
gpio.setup(en2,gpio.OUT)
#pwm1=gpio.PWM(en1,100)
#pwm2=gpio.PWM(en2,100)

#Speech Variables:
""" RATE"""
#rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                        #printing current voice rate
# engine.setProperty('rate', 150)     # setting up new voice rate
#
#
# """VOLUME"""
# volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# print (volume)                          #printing current volume level
# engine.setProperty('volume',10.0)    # setting up volume level  between 0 and 1
#
# """VOICE"""
# voices = engine.getProperty('voices')       #getting details of current voice
# #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[2].id)   #changing index, changes voices. 1 for female

Falcon = tinyik.Actuator(
    [
        "z",
        [0.0, 0.0, 0.25],
        "y",
        [13, 0.0, 0.0],
        "y",
        [9.05, 0.0, 0.0],
        "x",
        [3.23, 0.0, 0.0],
        "y",
        [14, 0.0, 0.0],
    ]
)
###Defining Functions:
def IK(x,y,z):
    Falcon.ee = [x , y , z]
    Falcon.angles = np.round(np.rad2deg(Falcon.angles))
    return Falcon.angles 
    
def ArmIk(a,b,c,d,e,f):
    # joint 0:
    ##servo0.angle =a
    #time.sleep(tsll)
    # joint 4:
    ##servo4.angle =e
    #time.sleep(tsll)
    # joint 2:
    ##servo2.angle =c
    time.sleep(tsh)
    # joint 1:
    ##servo1.angle =b
    #time.sleep(tsll)
    # joint 3:
    ##servo3.angle =d
    # joint 5:
    #servo5.angle =f
    
def ArmCameraStart():
    print ("CameraOne")    
    # joint 0:
    print("Channel0")
    #servo0.angle =75
    time.sleep(tsll)
    # joint 1:
    print("Channel1")
    #servo1.angle =120
    time.sleep(tsll)
    # joint 2:
    print("Channel2")
    #servo2.angle =180
    time.sleep(tsl)
    # joint 3:
    print("Channel3")
    #servo3.angle =90
    # joint 4:
    print("Channel4")
    #servo4.angle =20
    time.sleep(tsll)
    # joint 5:
    print("Channel5")
    #servo5.angle =0
    
    
def Zero():
    print ("CameraOne")    
    # joint 0:
    print("Channel0")
    #servo0.angle =80
    time.sleep(tsll)
    # joint 1:
    print("Channel1")
    #servo1.angle =46-3
    time.sleep(tsll)
    # joint 2:
    print("Channel2")
    #servo2.angle =30
    time.sleep(tsl)
    # joint 3:
    print("Channel3")
    #servo3.angle =2+90
    # joint 4:
    print("Channel4")
    #servo4.angle =35+90
    time.sleep(tsll)
    # joint 5:
    print("Channel5")
    #servo5.angle =40
    
def Forward(speed1, speed2=None):
    if speed2 is None:
        speed2 = speed1
    gpio.setmode(gpio.BCM)
    gpio.setup(in1, gpio.OUT)
    gpio.setup(in2, gpio.OUT)
    gpio.setup(in3, gpio.OUT)
    gpio.setup(in4, gpio.OUT)
    gpio.setup(en1,gpio.OUT)
    gpio.setup(en2,gpio.OUT)
    pwm1=gpio.PWM(en1,100)
    pwm2=gpio.PWM(en2,100)
    pwm1.start(speed1) # right
    pwm2.start(speed2) # left

    gpio.output(in1, False)
    gpio.output(in2, True)
    gpio.output(in3, False)
    gpio.output(in4, True) 
    print("FORWARD")
    #time.sleep(0.5)
        
def Backward(speed):
    gpio.setmode(gpio.BCM)
    gpio.setup(in1, gpio.OUT)
    gpio.setup(in2, gpio.OUT)
    gpio.setup(in3, gpio.OUT)
    gpio.setup(in4, gpio.OUT)
    gpio.setup(en1,gpio.OUT)
    gpio.setup(en2,gpio.OUT)
    pwm1=gpio.PWM(en1,00)
    pwm2=gpio.PWM(en2,00)
    pwm1.start(speed)
    pwm2.start(speed)

    gpio.output(in1, True)
    gpio.output(in2, False)
    gpio.output(in3, True)
    gpio.output(in4, False)
    print("BACKWARD")
    #time.sleep(0.5)

def TurnRight(speed,max_speed):
    gpio.setmode(gpio.BCM)
    gpio.setup(in1, gpio.OUT)
    gpio.setup(in2, gpio.OUT)
    gpio.setup(in3, gpio.OUT)
    gpio.setup(in4, gpio.OUT)
    gpio.setup(en1,gpio.OUT)
    gpio.setup(en2,gpio.OUT)
    pwm1=gpio.PWM(en1,100)
    pwm2=gpio.PWM(en2,100)
    pwm1.start(speed)
    pwm2.start(max_speed)

    gpio.output(in1, True)
    gpio.output(in2, False)
    gpio.output(in3, False)
    gpio.output(in4, True)
    print("TURNRIGHT")
    #time.sleep(0.5)
   
def TurnLeft(speed,max_speed):
    gpio.setmode(gpio.BCM)
    gpio.setup(in1, gpio.OUT)
    gpio.setup(in2, gpio.OUT)
    gpio.setup(in3, gpio.OUT)
    gpio.setup(in4, gpio.OUT)
    gpio.setup(en1,gpio.OUT)
    gpio.setup(en2,gpio.OUT)
    pwm1=gpio.PWM(en1,100)
    pwm2=gpio.PWM(en2,100)
    pwm1.start(max_speed)
    pwm2.start(speed)

    gpio.output(in1, False)
    gpio.output(in2, True)
    gpio.output(in3, True)
    gpio.output(in4, False)
    print("TURNLEFT")
    #time.sleep(0.5)
      
def Stop():
    gpio.setmode(gpio.BCM)
    gpio.setup(in1, gpio.OUT)
    gpio.setup(in2, gpio.OUT)
    gpio.setup(in3, gpio.OUT)
    gpio.setup(in4, gpio.OUT)
    
    gpio.output(in1, False)
    gpio.output(in2, False)
    gpio.output(in3, False)
    gpio.output(in4, False)
    gpio.cleanup()
    
def Cleanup():
    gpio.cleanup()
        
#Lights:
def FrontLight():
    print ("FRONT LED")    
    #pwm.set_pwm(8, 6000, 1500)
    #pwm.set_pwm(9, 0, 0)
    #pwm.set_pwm(10, 0, 0)
    #pwm.set_pwm(11, 0, 0)
    
def BackLight():
    print ("STOP")    
    #pwm.set_pwm(8, 0, 0)
    #pwm.set_pwm(9, 0, 0)
    #pwm.set_pwm(10, 0, 0)
    #pwm.set_pwm(11, 6000, 1500)

def RightLight():   
    print ("RIGHT LED")    
    #pwm.set_pwm(8, 0, 0)
    #pwm.set_pwm(9, 6000, 1500)
    time.sleep(0.4)
    #pwm.set_pwm(9, 0, 0)
    time.sleep(0.4)
    #pwm.set_pwm(10, 0, 0)
    #pwm.set_pwm(11, 0, 0)
    #
def LeftLight():   
    print ("LEFT LED") 
    #pwm.set_pwm(8, 0, 0)
    #pwm.set_pwm(9, 0, 0)
    #pwm.set_pwm(10, 6000, 1500)
    time.sleep(0.4)
    #pwm.set_pwm(10, 0, 0)
    time.sleep(0.4)
    #pwm.set_pwm(11, 0, 0)
        
def Homing():
    ArmHoming()
    time.sleep(0.1)
    ArmHoming()
    time.sleep(0.1)
    ArmHoming()
    time.sleep(0.1)
def ArmHoming():
    print ("HOMING")    
    # joint 0:
    print("Channel0")
    #servo0.angle =75
    time.sleep(tsll)
    # joint 2:
    print("Channel2")
    #servo2.angle =120
    time.sleep(tsl)
    # joint 1:
    print("Channel1")
    #servo1.angle =90
    time.sleep(tsll)
    # joint 3:
    print("Channel3")
    #servo3.angle =90
    time.sleep(tsll)
    # joint 4:
    print("Channel4")
    #servo4.angle =90
    time.sleep(tsll)
    # joint 5:
    print("Channel5")   
    #servo5.angle =0
    time.sleep(tsll)
    #servo5.angle =60
    time.sleep(tsll)
    

    
def ArmCameraDone():
    print ("CameraTwo")
    # joint 0:
    print("Channel0")
    #servo0.angle=75
    time.sleep(tsl)
    # joint 4:
    print("Channel4")
    #servo4.angle =130
    # joint 2:
    print("Channel2")
    #servo2.angle =90
    time.sleep(2)
    # joint 1:
    print("Channel1")
    #servo1.angle =50
    time.sleep(tsh)
    # joint 3:
    print("Channel3")
    #servo3.angle =90
    time.sleep(tsh)
    # joint 5:
    print("Channel5")
    #servo5.angle = 90
      
def PickStart():
    print ("I am PICKING")    
    # joint 4:
    print("Channel4")
    #servo4.angle =130
    # joint 0:
    print("Channel0")
    #servo0.angle=75
    time.sleep(tsh)
    # joint 2:
    print("Channel2")
    #servo2.angle =90
    time.sleep(tsh)
    # joint 1:
    print("Channel1")
    #servo1.angle =7
    time.sleep(tsh)
    # joint 3:
    print("Channel3")
    #servo3.angle =90
    # joint 5:
    print("Channel5")
    #servo5.angle = 20
    
def PickDone():
    print ("PICKED!") 
     # joint 4:
    print("Channel4")
    #servo4.angle =140
    # joint 0:
    print("Channel0")
    #servo0.angle=75
    time.sleep(tsh)
    # joint 2:
    print("Channel2")
    #servo2.angle =90
    time.sleep(tsh)
    # joint 1:
    print("Channel1")
    #servo1.angle =90
    time.sleep(tsh)
    # joint 3:
    print("Channel3")
    #servo3.angle =90
    time.sleep(tsh)
    # joint 5:
    print("Channel5")
    #servo5.angle = 20

# def SpeakBegin():
#     engine.say("Step Back.. Falcon is detecting!")
#     engine.runAndWait()
#     engine.stop()
#
# def SpeakColor():
#     engine.say("The Color is RED")
#     engine.runAndWait()
#     engine.stop()
#     
# def Speak(text):
#     str(text)
#     engine.say(text)
#     engine.runAndWait()
#     engine.stop()
# def SpeakSave(text):
#     """Saving Voice to a file"""
#     str(text)
#     engine.save_to_file( text , 'Saved.mp3')
#     engine.runAndWait()

doorPin = 1111 # change to the pin please
gpio.setup(doorPin, gpio.OUT)
def openDoor():
    gpio.output(doorPin,True)

def closeDoor():
    gpio.output(doorPin,False)

if __name__ == "__main__":
    gpio.setmode(gpio.BCM)
    gpio.setup(in1, gpio.OUT)
    gpio.setup(in2, gpio.OUT)
    gpio.setup(in3, gpio.OUT)
    gpio.setup(in4, gpio.OUT)
    gpio.setup(en1,gpio.OUT)
    gpio.setup(en2,gpio.OUT)
    gpio.setup(26,gpio.OUT)
    try:
        while True:
            Forward(100);
            #gpio.output(26, False)
    except KeyboardInterrupt:
        Cleanup()

