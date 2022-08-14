from gpiozero import Robot, LineSensor
from time import sleep
robot = Robot(left=(7, 8), right=(9, 10))
left_sensor = LineSensor(17)
right_sensor = LineSensor(27)
speed=0.65
def motor_speed():
    while True:
        left_detect = int(left_sensor.value)
        right_detect = int(right_sensor.value)
        if left_detect == 0 and right_detect == 0:
            left_mot = 1
            right_mot = 1
        ## Stage 2
        if left_detect == 0 and right_detect == 1:
            left_mot = -1
        if left_detect == 1 and right_detect == 0:
            right_mot = -1
        # print(r, l)
        yield (right_mot, left_mot, speed)

robot.source = motor_speed()

sleep(60)
robot.stop()
robot.source = None
robot.close()
left_sensor.close()
right_sensor.close()