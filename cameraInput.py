import cv2
from threading import Thread
from time import sleep

class camera(Thread):
    def __init__(self):
        self.frame= None
        self.webcam = cv2.VideoCapture(0)
        self.on = False
        super().__init__()

    def start(self):
        Thread(target=self.run,args=()).start()
        return self

    def run(self):
        self.on = True
        self.webcam.set(3, 160)
        self.webcam.set(4, 120)
        self.webcam.set(cv2.CAP_PROP_AUTO_EXPOSURE,0)
        self.webcam.set(cv2.CAP_PROP_AUTO_WB,0)
        while self.on:
            self.frame = self.webcam.read()[1]

    def stop(self):
        self.on = False
        cv2.destroyAllWindows()
        self.webcam.release()


if __name__== "__main__":
    cameraThread = camera()
    cameraThread.start()
    sleep(3)
    while (True):
        cv2.imshow("test",cameraThread.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cameraThread.stop()
            break

