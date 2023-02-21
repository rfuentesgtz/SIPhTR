import numpy
from picamera2 import Picamera2, Preview
from libcamera import controls
import cv2
import time

try:
    picam2 = Picamera2()
    picam2.start()
    picam2.set_controls({'AfMode': controls.AfModeEnum.Continuous})
    time.sleep(1)
except:
    print("Unable to start camera. Exiting...")
    exit()

while True:
    array = picam2.capture_array("main")

    image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    height, width, channels = image_bgr.shape
    cx = int(width / 2)
    cy = int(height / 2)

    pixelCenter = image_hsv[cy, cx]
    hueValue = pixelCenter[0]

    color = 'default'
        
    if(hueValue < 15):
        color = 'Red'
    elif (hueValue < 25):
        color = 'Orange'
    elif (hueValue < 35):
        color = 'Yellow'
    elif(hueValue < 45):
        color = 'Light Green'
    elif(hueValue < 75):
        color = 'Green'
    elif(hueValue < 83):
        color = 'Turquoise'
    elif(hueValue < 95):
        color = 'Light Blue'
    elif(hueValue < 135):
        color = 'Blue'
    elif(hueValue < 145):
        color = 'Purple'
    elif(hueValue < 155):
        color = 'Pink'
    elif(hueValue < 165):
        color = 'Magenta'
    elif(hueValue < 181):
        color = 'Red'
    
    saturation = pixelCenter[1]
    if(saturation < 80):
        color = 'White'
    
    value = pixelCenter[2]
    if(value < 30):
        color = 'Black'


    #print(array)

    cv2.putText(image_bgr, color, (5,50), 0, 1, (100,100,255), 2)
    cv2.circle(image_bgr, (cx , cy), 5, (255, 0, 0), 3)

    cv2.imshow("frame", image_bgr)

    if cv2.waitKey(1) == ord('q'):
        break


  
# closing all open windows
cv2.destroyAllWindows()
