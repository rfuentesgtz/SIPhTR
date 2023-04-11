import numpy
from picamera2 import Picamera2, Preview
from libcamera import controls
import cv2
import time

try:
    picam2 = Picamera2()
    config = picam2.create_video_configuration({"size": (1600, 900)})
    picam2.align_configuration(config)
    picam2.configure(config)
    picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition": 10000})
    picam2.start()
    time.sleep(1)
except:
    print("Unable to start camera. Exiting...")
    exit()

while True:
    array = picam2.capture_array("main")

    image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    cv2.imshow("frame", image_bgr)

    if cv2.waitKey(1) == ord('q'):
        cv2.imwrite("CoraVeryClose2.jpg", image_bgr)
        break