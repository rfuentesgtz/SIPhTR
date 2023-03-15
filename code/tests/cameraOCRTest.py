import tesserocr
from tesserocr import PyTessBaseAPI, PSM, OEM
import numpy
from picamera2 import Picamera2, Preview
import cv2
import time
import RPi.GPIO as GPIO 

from PIL import Image
from PIL import ImageOps
from libcamera import controls

in1 = 24
in2 = 23
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)


validText = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

print(tesserocr.tesseract_version())  # print tesseract-ocr version
#print(tesserocr.get_languages())  # prints tessdata path and list of available languages

picam2 = Picamera2()
picam2.start()
picam2.set_controls({'AfMode': controls.AfModeEnum.Continuous})
time.sleep(1)


with PyTessBaseAPI(psm=10) as api:
    #api.setPageSegMode()
    api.SetVariable('tessedit_char_whitelist', validText)

    while True:
        array = picam2.capture_array("main")
        image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        height, width, channels = image_rgb.shape

        #Find the coordinates for the center
        cx = int(width / 4)
        cy = int(height / 4)
        
        #Create a cropped copy of the image
        copy = image_rgb[cy:3*cy, cx:3*cx]
        imPil = Image.fromarray(copy)
        imPilGray = ImageOps.grayscale(imPil)


        #imPil.show()
        #time.sleep(3)

        api.SetImage(imPilGray)
        text = api.GetUTF8Text()
        #cv2.rectangle(image_bgr, (cx,cy), (3*cx, 3*cy), (255,255,255), 5)
        if(text != "" and text != " "):
            print(text[0])
            if(text[0] == 'R'):
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                time.sleep(1)
            else:
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)

            
        
        #cv2.putText(image_bgr, text, (5,50), 0, 1, (100,100,255), 2)
        cv2.imshow("frame", image_bgr)
        if cv2.waitKey(1) == ord('q'):
            break
        

cv2.destroyAllWindows()
# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.