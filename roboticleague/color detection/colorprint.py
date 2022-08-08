#notice:
#import as a module and pass image from cam as argument to the scanColor function
#change the resizing coordinates

import numpy as np
import cv2

def scanColor(imageFrame):
    #getting smaller picture
    x1,y1=150,0
    x2,y2=500,300
    imageFrame = imageFrame[y1:y2,x1:x2]
    #bgr to hsv
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    avg_color_per_row = np.average(hsvFrame, axis=0) 
    avg_color = np.average(avg_color_per_row, axis=0)

    red_lower1 = np.array([0, 87, 111], np.uint8)
    red_upper1 = np.array([25, 255, 255], np.uint8) 

    red_lower = np.array([156, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8) 

    green_lower = np.array([30, 52, 72], np.uint8)
    green_upper = np.array([92, 255, 255], np.uint8)

    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)

    if  ((np.less_equal(avg_color,red_upper1)).all() and (np.greater_equal(avg_color,red_lower1)).all()) or ((np.less_equal(avg_color,red_upper)).all() and (np.greater_equal(avg_color,red_lower)).all()):
            return 'R'

    elif (np.less_equal(avg_color,green_upper)).all() and (np.greater_equal(avg_color,green_lower)).all():
            return 'G'

    elif (np.less_equal(avg_color,blue_upper)).all() and (np.greater_equal(avg_color,blue_lower)).all():
            return 'B'


    # Program Termination
if __name__ == '__main__':
    webcam = cv2.VideoCapture(0)
    while(True):
        _, imageFrame = webcam.read()
        print(scanColor(imageFrame))
        cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break



