import numpy as np
import cv2
import Adafruit_BBIO.GPIO as GPIO

class line_follow():
    def __init__(self):
        self.cx = None
        self.cy = None
        self.no_line= False
        self.frame= None

    def start (self):
        Thread(target=self.run, args=()).start()
        return self

    def run(self):
        while (True):
            # Capture the frames
            #ret, frame = video_capture.read()
            # Crop the image
            crop_img = self.frame[60:120, 0:160]
            # Convert to grayscale
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            # Gaussian blur
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            # Color thresholding
            ret, thresh1 = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
            # Erode and dilate to remove accidental line detections
            mask = cv2.erode(thresh1, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            # Find the contours of the frame
            contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
            # Find the biggest contour (if detected)
            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                self.cx = int(M['m10'] / M['m00'])
                self.cy = int(M['m01'] / M['m00'])
                #cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)
                #cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)
                #cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)

            else:
                self.no_line = True


    def stop(self):
        self.on = False


