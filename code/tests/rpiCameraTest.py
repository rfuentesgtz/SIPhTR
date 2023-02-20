#This file is a quick test to ensure that 
#Picamera 2 can detect the camera, and
#move an actuator when it sees red
import RPi.GPIO as GPIO          

import numpy
from picamera2 import Picamera2, Preview
import cv2
import time

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

picam2 = Picamera2()
picam2.start()
time.sleep(1)

while True:
    array = picam2.capture_array("main")

    image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    height, width, channels = image_bgr.shape
    cx = int(width / 2)
    cy = int(height / 2)

    pixelCenter = image_hsv[cy, cx]
    hueValue = pixelCenter[0]

    if(hueValue < 15 or hueValue > 170):
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
    else:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)


    #print(array)

    cv2.imshow("frame", image_bgr)

    if cv2.waitKey(1) == ord('q'):
        break


  
# closing all open windows
cv2.destroyAllWindows()
GPIO.cleanup()
