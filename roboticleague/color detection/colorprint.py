#notice:
#import as a module and pass image from cam as argument to the scanColor function
#change the resizing coordinates

import numpy as np
import cv2

x1,y1=150,0
x2,y2=500,300

def scanColor(imageFrame):
    while True
        #delay to improve threading, removes stress from cpu
        time.delay(0.1)
        #getting smaller picture
        imageFrame = imageFrame[y1:y2,x1:x2]
        #bgr to hsv
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    #getting avg color from frame, might consider using dominant color
        avg_color_per_row = np.average(hsvFrame, axis=0) 
        avg_color = np.average(avg_color_per_row, axis=0)

    #color ranges: hsv (180,255,255)max
    #red has a part in beginning and the end of hue spectrum so two ranges are needed
    #use HSV_Treshhold.py to get calibrated values
        red_lower1 = np.array([0, 87, 111], np.uint8)
        red_upper1 = np.array([25, 255, 255], np.uint8) 

        red_lower = np.array([156, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8) 

        green_lower = np.array([30, 52, 72], np.uint8)
        green_upper = np.array([92, 255, 255], np.uint8)

        blue_lower = np.array([94, 80, 2], np.uint8)
        blue_upper = np.array([120, 255, 255], np.uint8)

    #test the avg color with each color range

        print(avg_color)
        if  ((np.less_equal(avg_color,red_upper1)).all() and (np.greater_equal(avg_color,red_lower1)).all()) or ((np.less_equal(avg_color,red_upper)).all() and (np.greater_equal(avg_color,red_lower)).all()):
                return 'R'

        elif (np.less_equal(avg_color,green_upper)).all() and (np.greater_equal(avg_color,green_lower)).all():
                return 'G'

        elif (np.less_equal(avg_color,blue_upper)).all() and (np.greater_equal(avg_color,blue_lower)).all():
                return 'B'

#code that runs when running this file directly
#if __name__ == '__main__':
#    webcam = cv2.VideoCapture(0)
#    while(True):
#        _, imageFrame = webcam.read()
#        print(scanColor(imageFrame))
#       cv2.imshow("test", imageFrame)
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#                webcam.release()
#                cv2.destroyAllWindows()
#                break
