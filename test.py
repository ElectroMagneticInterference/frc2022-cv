from types import NoneType
import threading
import cv2 as cv
import numpy as np
from time import sleep, time, time_ns
import cursor

# from src.daemon import pint


def process_image(image_bgr):
    start = time()

    if type(image_bgr) == NoneType:
        return

    image_hls = cv.cvtColor(image_bgr, cv.COLOR_BGR2HLS)

    inRange = cv.inRange(
        image_hls,
        (
            150,
            cv.threshold(cv.split(image_hls)[1], None, None, cv.THRESH_TRIANGLE)[0]
            - 10,
            150,
        ),
        (200, 255, 255),
    )

    # cv2.imshow(f"Image {i} : Thresholded", inRange)

    opened = cv.morphologyEx(
        cv.morphologyEx(inRange, cv.MORPH_CLOSE, np.ones((2, 2)), iterations=2),
        cv.MORPH_OPEN,
        np.ones((2, 2)),
        iterations=1,
    )

    print(time() - start, end="\r")

    contours, _ = cv.findContours(opened, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if not len(contours) > 0:
        # print("no contours found")
        cv.waitKey()
        cv.destroyAllWindows()
        return opened

    largest = contours[0]
    for contour in contours:
        if cv.contourArea(contour) > cv.contourArea(largest):
            largest = contour

    new_image = cv.drawContours(image_bgr, largest, -1, (0, 0, 255), 3, offset=(0, -3))

    rect = cv.minAreaRect(largest)
    center, _, _ = rect
    center = (int(center[0]), int(center[1] - 25))

    new_image = cv.circle(image_bgr, center, 10, (0, 255, 0), thickness=-1)

    # cv2.imshow(f"Image {i} : Contours", new_image)

    cv.waitKey()

    cv.destroyAllWindows()

    print()
    return new_image


"""
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  """


class stoppable_thread(threading.Thread):
    __running__ = True
    __name__ = None

    def init(self):
        super().__init__(target=self.run, name=self.name, daemon=True)
        self.start()

    def stop(self):
        self.__running__ = False


processed_frames = []


class display_thread(stoppable_thread):
    __name__ = "Display-Thread"

    def run(self):
        while self.running:
            if len(processed_frames):
                cv.imshow("FRC Vision - Webcam", processed_frames.pop(0))

                if cv.waitKey(1) == ord("q"):
                    self.running = False


unprocessed_frames = []

processing_thread_count = 0


def process_thread_number():
    global processing_thread_count
    processing_thread_count += 1
    return processing_thread_count


class processing_thread(stoppable_thread):
    __name__ = f"Process-Thread{process_thread_number()}"

    def run(self):
        global processing_thread_count

        while self.__running__:
            # if there are no unprocessed frames, yield to other threads and restart loop
            if not len(unprocessed_frames):
                sleep(0)
                continue

            # else: process the first image on the frame stack

            processed_image = process_image(unprocessed_frames.pop(0))

            # get current time
            end_time = time_ns()

            # if there are processed frames
            if len(processed_frames):
                end = False
                for i, pf in enumerate(processed_frames):
                    if end_time <= pf[0]:
                        processed_frames.insert(i, processed_image)
                        end = True
                        break
                if end:
                    break

            processed_frames.append([end_time, processed_image])

        processing_thread_count -= 1


class capture_thread(stoppable_thread):
    booting = True
    __name__ = "Capture-Thread"

    def run(self):
        cam = cv.VideoCapture(0)

        if not cam:
            raise Exception("Camera failed to connect!")

        display_thread().start()

        self.booting = False

        while self.__running__:
            result, frame = cam.read()
            if result:
                processing_thread(frame)

        display_thread.stop()


import cv


cursor.hide()
cv.startWindowThread()

capt = capture_thread()

capt.start()

while capt.booting:
    sleep(1)

cv.waitKey(0)
cursor.show()
cv.destroyAllWindows()
