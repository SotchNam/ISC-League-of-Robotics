import time
import numpy as np
import cv2
from threading import Thread

class line_follow(Thread):
    def __init__(self):
        self.cx = None
        self.cy = None
        self.no_line= False
        self.frame= None
        self.on = False
        self.circle= False
        self.croppedImage = None
        super().__init__()

    def start (self):
        Thread(target=self.run, args=()).start()
        return self

    def run(self):
        self.on = True
        while self.on:
            # Capture the frames
            #ret, frame = video_capture.read()
                #print("line frame:")
                #print(self.frame)

            try:
                # Crop the image
                #crop_img = self.frame[60:120, 0:160]
                self.croppedImage = self.frame[120:240, 0:320]
                # Convert to grayscale
                gray = cv2.cvtColor(self.croppedImage, cv2.COLOR_BGR2GRAY)
                # Gaussian blur
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                # Color thresholding
                ret, thresh1 = cv2.threshold(blur, 24, 255, cv2.THRESH_BINARY_INV)
                # Erode and dilate to remove accidental line detections
                mask = cv2.erode(thresh1, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                # Find the contours of the frame
                contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

                # end circle detection
                circle = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=30, minRadius=50, maxRadius=70)
                if circle is not None:
                    self.circle = True
                else:
                    self.circle=False

                # Find the biggest contour (if detected)
                if len(contours) > 0:
                    self.no_line = False
                    c = max(contours, key=cv2.contourArea)
                    M = cv2.moments(c)
                    self.cx = int(M['m10'] / M['m00'])
                    self.cy = int(M['m01'] / M['m00'])
                    #cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)
                    #cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)
                    #cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)

                #elif self.circle is not None:
                    #self.circle = True

                else:
                    self.no_line = True

            except TypeError:
                print("Line: no frame")


    def stop(self):
        self.on = False


if __name__ == '__main__':
    try:
        import RPi.GPIO as gpio
        import Falcon
        from main import forwardTimed
        webcam = cv2.VideoCapture(0)
        webcam.set(3, 320)
        webcam.set(4, 240)
        webcam.set(cv2.CAP_PROP_AUTO_EXPOSURE,0)
        webcam.set(cv2.CAP_PROP_AUTO_WB,0)


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
        imageWidth = 320 #lineThread.frame.shape[1] # = 320
        leftMostBound= imageWidth*0.255
        leftBound = imageWidth*0.45
        center = imageWidth / 2 # 80
        rightBound = imageWidth*0.55
        rightMostBound= imageWidth*0.705

        _, imageFrame = webcam.read()
        lineThread = line_follow()
        lineThread.frame = imageFrame
        lineThread.start()
        time.sleep(3)
        while(True):
            _, imageFrame = webcam.read()
            #imageFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2RGB)
            lineThread.frame = imageFrame
            #cv2.imshow("Frame", lineThread.croppedImage) 
            #cv2.imshow("test", imageFrame)
            print(lineThread.cx)


            try:
                if lineThread.no_line == False:
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
                    #Falcon.Stop() # continue previous action
                    #sleep(2) # enough time for line cut 15cm dist
            except TypeError:
                pass


            if cv2.waitKey(1) & 0xFF == ord('q'):
                    lineThread.stop()
                    webcam.release()
                    cv2.destroyAllWindows()
                    break
    except KeyboardInterrupt:
        lineThread.stop()
        webcam.release()
        cv2.destroyAllWindows()
