import numpy
from picamera2 import Picamera2, Preview
from libcamera import controls
import cv2
import time

try:
    picam2 = Picamera2()
    picam2.start()
    picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition": 10.0})
    time.sleep(1)
    objectDetector = cv2.createBackgroundSubtractorMOG2(history=120, varThreshold=60)
except:
    print("Unable to start camera. Exiting...")
    exit()

while True:
    array = picam2.capture_array("main")

    image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

    height = image_bgr.shape[0]
    width = image_bgr.shape[1]

    cropped = image_bgr[int(height/4):int(3*height/4), int(width/4):int(3*width/4)]

    mask = objectDetector.apply(cropped)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    x = 0
    y = 0
    w = 0
    h = 0
    roi = cropped

    tmpArea = -1
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if (area > 300):
            #cv2.drawContours(cropped, [cnt], -1, (0, 255, 0), 2)
            if(area > tmpArea):
                tmpArea = area
                x, y, w, h = cv2.boundingRect(cnt)
                
    if(tmpArea > 0):
        cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 0, 255), 3)
        roi = cropped[int(y):int(y + h), int(x):int(x+w)]    
    
    


    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    cv2.imshow("frame", image_bgr)
    cv2.imshow("frame2", cropped)
    #cv2.imshow("frame3", roi)

    if cv2.waitKey(1) == ord('q'):
        break


  
# closing all open windows
cv2.destroyAllWindows()
