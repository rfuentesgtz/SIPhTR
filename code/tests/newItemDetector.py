import numpy
from picamera2 import Picamera2, Preview
from libcamera import controls
import cv2
import time

try:
    picam2 = Picamera2()
    config = picam2.create_video_configuration({'size':(1600,720)})
    picam2.align_configuration(config)
    picam2.configure(config)
    picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition":9})#, 'LensPosition': 10})
    picam2.start()
    time.sleep(1)
    #objectDetector = cv2.createBackgroundSubtractorMOG2(history=150, varThreshold=35)
except:
    print("Unable to start camera. Exiting...")
    exit()

tempTime = time.time()
count = 0
timeReset = time.time() + 1
while True:
    if(time.time() > timeReset):
        print(count)
        count = 0
        timeReset = time.time() + 1
    array = picam2.capture_array("main")

    image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

    height = image_bgr.shape[0]
    width = image_bgr.shape[1]

    cropped = image_bgr#[int(height/4):int(3*height/4), int(width/4):int(3*width/4)]
    croppedGray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    croppedBlur = cv2.GaussianBlur(croppedGray, (5,5), 0)

    #mask = objectDetector.apply(cropped)
    _, mask = cv2.threshold(croppedBlur, 95, 255, cv2.THRESH_BINARY)

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
        if(area > tmpArea):
            tmpArea = area
            x, y, w, h = cv2.boundingRect(cnt)
            #cv2.drawContours(image_bgr, cnt, -1, (127,127,127), 15)
                
    if(tmpArea > 0 and w != 0 and h != 0 and (w / h > 0.4) and (h / w) > 0.4):
        cv2.rectangle(image_bgr, (x, y), (x + w, y + h), (0, 0, 255), 3)
        #roi = cropped[int(y):int(y + h), int(x):int(x+w)]
        cropHSV = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)    
        testPixel = cropHSV[int((y+h)/2), int((x+w)/2)]
        hueValue = testPixel[0]
            
        if(hueValue < 15):
            color = 'Red'
        elif (hueValue < 30):
            color = 'Orange'
        elif (hueValue < 45):
            color = 'Yellow'
        elif(hueValue < 60):
            color = 'Chastreuse'
        elif(hueValue < 75):
            color = 'Green'
        elif(hueValue < 90):
            color = 'Spring'
        elif(hueValue < 105):
            color = 'Cyan'
        elif(hueValue < 120):
            color = 'Azure'
        elif(hueValue < 135):
            color = 'Blue'
        elif(hueValue < 150):
            color = 'Purple'
        elif(hueValue < 165):
            color = 'Magenta'
        elif(hueValue < 181):
            color = 'Pink'
        
        saturation = testPixel[1]
        if(saturation < 25):
            color = 'White'
        
        value = testPixel[2]
        if(value < 10):
            color = 'Black'
    
    


    #image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    count = count + 1
    cv2.putText(image_bgr, color, (5,50), 0, 1, (255,255,255), 2)
    cv2.imshow("frame", image_bgr)
    #cv2.imshow("frame2", mask)
    #cv2.imshow("frame3", roi)

    if cv2.waitKey(1) == ord('q'):
        cv2.imwrite("ItemDetectColor3.jpg", cropped)
        break
    

  
# closing all open windows
cv2.destroyAllWindows()
