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

    height, width, channels = image_bgr.shape
    #Cover from 1/4 to 3/4
    cx = int(width / 4)
    cy = int(height / 4)

   #Create a cropped copy of the image
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    copy = gray[cy:3*cy, cx:3*cx]

    # setting threshold of gray image
    _, threshold = cv2.threshold(copy, 125, 255, cv2.THRESH_BINARY)

    #Blurring the image to detect less contours
    blur = cv2.GaussianBlur(threshold, (5,5), cv2.BORDER_DEFAULT)

    # using a findContours() function
    contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0

    value = 'unknown'

    for contour in contours:
        # here we are ignoring first counter because 
        # findcontour function detects whole image as shape
        if i == 0:
            i = 1
            continue

        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(contour, 0.03 * cv2.arcLength(contour, True), True)
        
        # using drawContours() function
        #cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)

        if(len(approx) == 3):
            value = 'Triangle'
        elif(len(approx) == 4):
            value = 'Square'
        elif(len(approx) == 5):
            value = 'Pentagon'
        elif(len(approx) == 10):
            value = 'Star'
        elif(len(approx) > 10 and len(approx) < 20):
            value = 'Circle'
    #print(array)

    cv2.putText(image_bgr, value, (5,50), 0, 1, (100,100,255), 2)
    cv2.rectangle(image_bgr, (cx,cy), (3*cx, 3*cy), (255,255,255), 5)

    cv2.imshow("frame", blur)

    if cv2.waitKey(1) == ord('q'):
        break


  
# closing all open windows
cv2.destroyAllWindows()
