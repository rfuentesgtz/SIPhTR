import numpy
import tesserocr
from tesserocr import PyTessBaseAPI, PSM, OEM
from picamera2 import Picamera2, Preview
from libcamera import controls
import cv2
import time
from PIL import Image
from PIL import ImageOps

try:
    picam2 = Picamera2()
    config = picam2.create_video_configuration()
    picam2.align_configuration(config)
    picam2.configure(config)
    picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition": 10})
    picam2.start()
    time.sleep(1)
    objectDetector = cv2.createBackgroundSubtractorMOG2(history=150, varThreshold=20)
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
        croppedRGB = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        mask = objectDetector.apply(cropped)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        x = 0
        y = 0
        w = 0
        h = 0
        roi = cropped
        character = "?"

        tmpArea = -1
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if (area > 3000):
                #cv2.drawContours(cropped, [cnt], -1, (0, 255, 0), 2)
                if(area > tmpArea):
                    tmpArea = area
                    x, y, w, h = cv2.boundingRect(cnt)
                    
        if(tmpArea > 0):
            cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 0, 255), 3)
            roi = cropped[int(y):int(y + h), int(x):int(x+w)]

            roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            imgGray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.blur(imgGray, (3,3))

            ret, imgBinary = cv2.threshold(imgBlur, 127, 255, cv2.THRESH_BINARY)
            imPil = Image.fromarray(croppedRGB)

            api.SetImage(imPil)
            conf = api.MeanTextConf()
            readCharacter = api.GetUTF8Text()

            if (conf > 30):
                if readCharacter[0] in chars:
                    chars[readCharacter[0]] = chars[readCharacter[0]] + 1
                else:
                    chars[readCharacter[0]] = 1
            
        if time.time() >= (timeVal + 2):
            for key, value in chars.items():
                chars[key] = 0
            chars["?"] = 1
            timeVal = time.time()

        #image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

        cv2.putText(cropped, max(chars, key=chars.get), (5,50), 0, 1, (100,100,255), 2)
        cv2.imshow("frame", image_bgr)
        cv2.imshow("frame2", cropped)
        #cv2.imshow("frame3", roi)

        if cv2.waitKey(1) == ord('q'):
            cv2.imwrite("ItemDetectOCR1.jpg", cropped)
            break


  
# closing all open windows
cv2.destroyAllWindows()
