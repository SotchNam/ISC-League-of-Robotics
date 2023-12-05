#notice:
#import as a module and pass image from cam as argument to the scanColor function
#change the resizing coordinates

from threading import Thread
import numpy as np
import cv2
import time

#using absolute resolution
#x1,y1=150,0
#x2,y2=500,300
#using relative resolution
x1,y1=0.3,0
x2,y2=0.4,0.25

class scanColor(Thread):
    def __init__(self):
        self.color= None
        self.frame= None
        self.on = False
        self.avgColor = None
        self.croppedImage = None
        super().__init__()

    def start(self):
        Thread(target=self.run,args=()).start()
        return self

    def run(self):
        #color ranges: hsv (180,255,255)max
        #red has a part in beginning and the end of hue spectrum so two ranges are needed
        #use HSV_Treshhold.py to get calibrated values
        red_lower1 = np.array([0, 87, 111], np.uint8)
        red_upper1 = np.array([25, 255, 255], np.uint8) 

        red_lower = np.array([160, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8) 

        green_lower = np.array([40, 52, 72], np.uint8)
        green_upper = np.array([92, 255, 255], np.uint8)

        blue_lower = np.array([94, 70, 82], np.uint8)
        blue_upper = np.array([121, 255, 255], np.uint8)

        self.on = True
        while self.on:
            #delay to improve threading, removes stress from cpu
            time.sleep(0.1)
            try:
                #getting smaller picture
                y= self.frame.shape[0]
                x= self.frame.shape[1]
                imageFrame = self.frame[int(y*y1):int(y*y2), int(x*x1):int(x*x2)]
                #imageFrame = self.frame[y1:y2,x1:x2]
                #bgr to hsv
                hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
                #getting avg color from frame, might consider using dominant color
                avg_color_per_row = np.average(hsvFrame, axis=0) 
                avg_color = np.average(avg_color_per_row, axis=0)
                self.avgColor = avg_color
                self.croppedImage = imageFrame
                print(avg_color)

                #test the avg color with each color range
                #print(self.frame)
                if  ((np.less_equal(avg_color,red_upper1)).all() and (np.greater_equal(avg_color,red_lower1)).all()) or ((np.less_equal(avg_color,red_upper)).all() and (np.greater_equal(avg_color,red_lower)).all()):
                        self.color= 'R'

                elif (np.less_equal(avg_color,green_upper)).all() and (np.greater_equal(avg_color,green_lower)).all():
                        self.color = 'G'

                elif (np.less_equal(avg_color,blue_upper)).all() and (np.greater_equal(avg_color,blue_lower)).all():
                        self.color = 'B'
                else:
                        self.color = None

            except TypeError:
                print("Color: No frame")

    def stop(self):
        self.on = False


if __name__ == '__main__':
    try:
        webcam = cv2.VideoCapture(0)
        webcam.set(3, 320)
        webcam.set(4, 240)
        webcam.set(cv2.CAP_PROP_AUTO_EXPOSURE,0)
        webcam.set(cv2.CAP_PROP_AUTO_WB,0)
        _, imageFrame = webcam.read()
        colorThread = scanColor()
        colorThread.frame = imageFrame
        colorThread.start()
        time.sleep(3)
        while(True):
            _, imageFrame = webcam.read()
            #imageFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2RGB)
            colorThread.frame = imageFrame
            cv2.imshow("Frame", colorThread.croppedImage) 
            cv2.imshow("test", imageFrame)
            print(colorThread.color)
            print(colorThread.avgColor)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                    colorThread.stop()
                    webcam.release()
                    cv2.destroyAllWindows()
                    break
    except KeyboardInterrupt:
        colorThread.stop()
        webcam.release()
        cv2.destroyAllWindows()

