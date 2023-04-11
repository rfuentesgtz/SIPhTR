import tesserocr
from tesserocr import PyTessBaseAPI, PSM, OEM
import numpy
from picamera2 import Picamera2, Preview
import cv2
import time
from libcamera import controls

from PIL import Image
from PIL import ImageOps

try:
    picam2 = Picamera2()
    config = picam2.create_video_configuration({"size": (1600, 900)})
    picam2.align_configuration(config)
    picam2.configure(config)
    picam2.set_controls({'AfMode': controls.AfModeEnum.Continuous})
    picam2.start()
    time.sleep(1)
except:
    print("Unable to start camera. Exiting...")
    exit()

validText = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
chars = {"?": 0}
with PyTessBaseAPI(psm=10) as api:
    api.SetVariable('tessedit_char_whitelist', validText)
    timeVal = time.time()
    while True:
        array = picam2.capture_array("main")

        image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        height = image_bgr.shape[0]
        width = image_bgr.shape[1]

        cropped = image_bgr[int(height/2 - height/8):int(height/2 + height/8), int(width/2 - width/8):int(width/2 + width/8)]
        imgGray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.blur(imgGray, (7,7))

        ret, imgBinary = cv2.threshold(imgBlur, 50, 255, cv2.THRESH_BINARY)
        imPil = Image.fromarray(imgGray)

        api.SetImage(imPil)
        conf = api.MeanTextConf()
        readCharacter = api.GetUTF8Text()

        if time.time() >= (timeVal + 2):
            for key, value in chars.items():
                chars[key] = 0
            chars["?"] = 1
            timeVal = time.time()

        if (conf > 40):
            if readCharacter[0] in chars:
                chars[readCharacter[0]] = chars[readCharacter[0]] + 1
            else:
                chars[readCharacter[0]] = 1

        cv2.putText(imgGray, max(chars, key=chars.get), (5,50), 0, 1, (100,100,255), 2)
        cv2.imshow("frame", imgGray)

        if cv2.waitKey(1) == ord('q'):
            break
