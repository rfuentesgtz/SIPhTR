import cv2 as cv
import numpy as np
import pytesseract

def sortByColor():
    print('Selected sorting by color')

    try:
        print('Starting up camera...')
        video = cv.VideoCapture(0)
    except:
        print('Video camera not found')
        return

    while (True):
        _, img = video.read()
        height, width, channels = img.shape

        #Create an HSV frame of the image
        hsv_frame = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        #Finf the coordinates for the center
        cx = int(width / 2)
        cy = int(height / 2)
        pixelCenter = hsv_frame[cy, cx]
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
        if(saturation < 100):
            color = 'White'
        
        value = pixelCenter[2]
        if(value < 50):
            color = 'Black'

        cv.putText(img, color, (5,50), 0, 1, (100,100,255), 2)
        cv.circle(img, (cx , cy), 5, (255, 0, 0), 3)
        cv.imshow('Video camera', img)
        key = cv.waitKey(1)

        if(key == 32):
            break
        #cv.destroyAllWindows()

        #print(hue_value)

def sortByShape():
    print('Selected sorting by shape')
    try:
        print('Starting up camera...')
        video = cv.VideoCapture(0)
    except:
        print('Video camera not found')
        return

    while (True):
        _, img = video.read()
        height, width, channels = img.shape

        #Find the coordinates for the center
        cx = int(width / 2)
        cy = int(height / 2)
        
        #Create a cropped copy of the image
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        copy = gray[cy-50:cy+50, cx-100:cx+100]

        # setting threshold of gray image
        _, threshold = cv.threshold(copy, 125, 255, cv.THRESH_BINARY)

        #Blurring the image to detect less contours
        blur = cv.GaussianBlur(threshold, (7,7), cv.BORDER_DEFAULT)
  
        # using a findContours() function
        contours, _ = cv.findContours(blur, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        i = 0

        value = 'unknown'

        for contour in contours:
            # here we are ignoring first counter because 
            # findcontour function detects whole image as shape
            if i == 0:
                i = 1
                continue
        
            # cv2.approxPloyDP() function to approximate the shape
            approx = cv.approxPolyDP(contour, 0.03 * cv.arcLength(contour, True), True)
            
            # using drawContours() function
            #cv.drawContours(img, [contour], 0, (0, 0, 255), 5)

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

        cv.putText(img, value, (5,50), 0, 1, (100,100,255), 2)
        cv.rectangle(img, (cx-100,cy-50), (cx + 100, cy + 50), (255,255,255), 5)
        cv.imshow('Video camera', img)
        key = cv.waitKey(1)

        if(key == 32):
            break
        #cv.destroyAllWindows()

        #print(hue_value)

def sortByOCR():
    print('Selected sorting by OCR')
    try:
        print('Starting up camera...')
        video = cv.VideoCapture(0)
        pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    except:
        print('Video camera not found')
        return

    while (True):
        _, img = video.read()
        #img = cv.imread('alphabet.png')
        height, width, channels = img.shape
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        #Finf the coordinates for the center
        cx = int(width / 2)
        cy = int(height / 2)

        #Create a cropped copy of the image
        copy = gray[cy-50:cy+50, cx-100:cx+100]

        readValue = 'Dummy'

        readValue = pytesseract.image_to_string(copy, config ='--psm 6')
        cv.rectangle(img, (cx-100,cy-50), (cx + 100, cy + 50), (255,255,255), 5)
        cv.putText(img, readValue, (5,50), 0, 1, (100,100,255), 2)
        #cv.circle(img, (cx , cy), 5, (255, 0, 0), 3)
        #cv.imshow('Video camera', copy)
        cv.imshow('Video camera', img)
        key = cv.waitKey(1)

        if(key == 32):
            break
        #cv.destroyAllWindows()

        #print(hue_value)




print('Select your mode of operation.')
print('1: Color')
print('2: Shape')
print('3: OCR')
userInput = input('Make your choice: ')
selection = int(userInput.strip())

if(selection == 1):
    sortByColor()

elif(selection == 2):
    sortByShape()

elif(selection == 3):
    sortByOCR()

else:
    print('Invalid selection')

