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
    picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition": 11})
    picam2.start()
    time.sleep(1)
    objectDetector = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=15)
except:
    print("Unable to start camera. Exiting...")
    exit()

while True:
    array = picam2.capture_array("main")

    image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

    height = image_bgr.shape[0]
    width = image_bgr.shape[1]

    cropped = image_bgr[int(height/2 - height/3):int(height/2 + height/3), int(width/2 - width/7.25):int(width/2 + width/7.25)]
    croppedBlur = cv2.GaussianBlur(cropped, (5,5), 0.2)

    croppedGray = cv2.cvtColor(croppedBlur, cv2.COLOR_BGR2GRAY)
    

    mask = objectDetector.apply(cropped)
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    x = 0
    y = 0
    w = 0
    h = 0
    roi = cropped
    shape = "default"

    tmpArea = -1
    i=0
    shapeContour = 0
    avgLength = 0
    valueInMM = 0
    for cnt in contours:
        if i == 0:
            i = 1
            continue
        area = cv2.contourArea(cnt)
        if (area > 5000):
            #cv2.drawContours(cropped, [cnt], -1, (0, 255, 0), 2)
            if(area > tmpArea):
                tmpArea = area
                shapeContour = cnt
                x, y, w, h = cv2.boundingRect(cnt)
                
    if(tmpArea > 0):
        cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 0, 255), 3)
        avgLength = ((w-x) + (h-y)) / 2.0
        valueInMM = avgLength / 18.25

        #roundedLength = (valueInMM * 2) / 2
        #print(roundedLength)
        #cv2.drawContours(cropped, shapeContour, -1, (255, 155, 255))
        #approx = cv2.approxPolyDP(shapeContour, 0.05 * cv2.arcLength(shapeContour, True), True)
        #cv2.drawContours(cropped, approx, -1, (255, 255, 255))
        roi = croppedGray#[int(y):int(y + h), int(x):int(x+w)]
        _, roiThresh = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY)
        contours2, _ = cv2.findContours(roiThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        j = 0

        for cnt2 in contours2:
            if j == 0:
                j = 1
                continue
            if (cv2.contourArea(cnt2) > 2000):
                #cv2.imshow("Thresh", roiThresh)
                approx = cv2.approxPolyDP(cnt2, 0.03 * cv2.arcLength(cnt2, True), True)
                #cv2.drawContours(cropped, cnt2, -1, (255,255,255), 5)
                #time.sleep(0.10)
                if len(approx) == 3:
                    shape = "triangle"
                elif len(approx) == 4:
                    shape = "square"
                elif len(approx) == 10:
                    shape = "star"
                if len(approx) > 11:
                    shape = "circle"
                #shape = shape + "," + str(len(approx))
                #time.sleep(0.10)
                shape = shape + ', ' + str(valueInMM)
                    
                                                                                                                                                                                                                                                                                                 

        #roi = cropped[int(y):int(y + h), int(x):int(x+w)]

    
    


    #image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    cv2.putText(cropped, shape, (5,50), 0, 1, (255,255,255), 2)
    cv2.imshow("frame", image_bgr)
    cv2.imshow("frame2", cropped)
    if(valueInMM > 14.75 and valueInMM < 15.25 and shape != "default"):
        cv2.imwrite("ItemDetectShape.jpg", cropped)
    #cv2.imshow("frame3", roi)

    if cv2.waitKey(1) == ord('q'):
        cv2.imwrite("ItemDetectShape.jpg", cropped)
        break


  
# closing all open windows
cv2.destroyAllWindows()
