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
        while self.on:
            _, self.frame = self.webcam.read()
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

    def stop(self):
        self.on = False
        cv2.destroyAllWindows()
        self.webcam.release()


if __name__== "__main__":
    cameraThread = camera()
    cameraThread.start()
    sleep(1)
    while (True):
        cv2.imshow("test",cameraThread.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cameraThread.stop()
            break

