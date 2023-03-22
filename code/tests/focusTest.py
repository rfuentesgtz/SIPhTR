import numpy
from picamera2 import Picamera2, Preview
from libcamera import controls
import cv2
import time

try:
    picam2 = Picamera2()
    picam2.start()
    picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition": 4000.0})
    time.sleep(1)
except:
    print("Unable to start camera. Exiting...")
    exit()

while True:
    array = picam2.capture_array("main")

    image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    cv2.imshow("frame", image_bgr)

    if cv2.waitKey(1) == ord('q'):
        break