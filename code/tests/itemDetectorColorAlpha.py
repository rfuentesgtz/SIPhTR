import numpy
from picamera2 import Picamera2, Preview
from libcamera import controls
import cv2
import time

try:
    picam2 = Picamera2()
    config = picam2.create_preview_configuration()
    picam2.align_configuration(config)
    picam2.configure(config)
    picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition": 10})
    picam2.start()
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
    color = "default"

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
        #roi = cropped[int(y):int(y + h), int(x):int(x+w)]
        cropHSV = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)    
        testPixel = cropHSV[int((y+h)/2), int((x+w)/2)]
        hueValue = testPixel[0]
            
        if(hueValue < 5):
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
        
        saturation = testPixel[1]
        if(saturation < 80):
            color = 'White'
        
        value = testPixel[2]
        if(value < 30):
            color = 'Black'
    
    


    #image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    cv2.putText(cropped, color, (5,50), 0, 1, (255,255,255), 2)
    cv2.imshow("frame", image_bgr)
    cv2.imshow("frame2", cropped)
    #cv2.imshow("frame3", roi)

    if cv2.waitKey(1) == ord('q'):
        cv2.imwrite("ItemDetectColor3.jpg", cropped)
        break


  
# closing all open windows
cv2.destroyAllWindows()