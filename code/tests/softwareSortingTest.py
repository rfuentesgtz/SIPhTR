#Import Libraries

import numpy
import tesserocr
from tesserocr import PyTessBaseAPI, PSM, OEM
from picamera2 import Picamera2, Preview
from libcamera import controls
import cv2
import time
from PIL import Image
from PIL import ImageOps
import json
import os
from datetime import date
from datetime import datetime

#----------JSON FILE CREATION----------
#Main directory
storageDirectory = "/home/siphtr/Documents/siphtrResults"
if(not os.path.exists(storageDirectory)):
    print("Making folders")
    os.mkdir(storageDirectory)
day = date.today().strftime("%Y_%m_%d")
outputFolder = storageDirectory + "/" + day
if(not os.path.exists(outputFolder)):
    print("Making directory 2")
    os.mkdir(outputFolder)
currentTime = datetime.now().strftime("%H_%M_%S")
outputFileFullPath = outputFolder + "/" + currentTime + ".json"


#----------COLOR SORTING FUNCTION DEFINITION----------
def sortByColor(image):
    height1, width1, channels = image.shape
    color = "default"
    if(height1 == 0 or width1 == 0):
        return color
    cropHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    
    testPixel = cropHSV[int((height1)/2), int((width1)/2)]
    hueValue = testPixel[0]
        
    if(hueValue < 5):
        color = 'Red'
    elif (hueValue < 25):
        color = 'Orange'
    elif (hueValue < 40):
        color = 'Yellow'
    elif(hueValue < 60):
        color = 'Chastreuse'
    elif(hueValue < 75):
        color = 'Green'
    elif(hueValue < 90):
        color = 'Spring'
    elif(hueValue < 100):
        color = 'Cyan'
    elif(hueValue < 135):
        color = 'Blue'
    elif(hueValue < 150):
        color = 'Purple'
    elif(hueValue < 165):
        color = 'Magenta'
    elif(hueValue < 176):
        color = 'Pink'
    elif(hueValue < 181):
        color = "Red"
    
    saturation = testPixel[1]
    if(saturation < 50):
        color = 'White'
    
    value = testPixel[2]
    if(value < 55):
        color = 'Black'

    return(color)


#----------Shape/Size SORTING FUNCTION DEFINITION----------
def sortByShapeSize(image, contour):
    height1, width1, channels = image.shape
    shape = "?"
    if(height1 == 0 or width1 == 0):
        return shape
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

    #cv2.drawContours(cropped, cnt2, -1, (255,255,255), 5)
    #time.sleep(0.10)
    print(len(approx))
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
    #shape = shape + ', ' + str(valueInMM)
    return shape


#----------OCR SORTING FUNCTION DEFINITION----------
def sortByOCR(image, api):
    height1, width1, channels = image.shape
    readCharacter = "?"
    if(height1 == 0 or width1 == 0):
        return readCharacter
    imPil = Image.fromarray(image)
    imPilGray = ImageOps.grayscale(imPil)

    api.SetImage(imPil)
    conf = api.MeanTextConf()
    if (conf > 40):
        readCharacter = api.GetUTF8Text()
    return readCharacter



with open(outputFileFullPath, "w") as outputFile:
    #Sample input for mode selection
    mode = int(input("Please enter your sorting mode.\n1: Color\n2: Shape/Size\n3: OCR\nAnswer: ").strip())


    #----------COLOR FOR LOOP----------
    #Configure pre-set values that change between modes
    if(mode == 1):
        #Initialize camera
        try:
            picam2 = Picamera2()
            config = picam2.create_video_configuration({'size':(1280,720)})
            picam2.align_configuration(config)
            picam2.configure(config)
            picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition":9})#, 'LensPosition': 10})
            picam2.start()
            time.sleep(1)
        except:
            print("Unable to start camera. Exiting...")
            exit()

        try:
            while True:
                #Capture a drame from the camera
                array = picam2.capture_array("main")

                image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

                height = image_bgr.shape[0]
                width = image_bgr.shape[1]

                cropped = image_bgr#[int(height/4):int(3*height/4), int(width/4):int(3*width/4)]
                croppedGray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                croppedBlur = cv2.GaussianBlur(croppedGray, (5,5), 0)

                #mask = objectDetector.apply(cropped)
                _, mask = cv2.threshold(croppedBlur, 127, 255, cv2.THRESH_BINARY)

                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                x = 0
                y = 0
                w = 0
                h = 0
                #roi = cropped
                color = "default"

                tmpArea = -1
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if(area > tmpArea and area > 5000):
                        tmpArea = area
                        xt, yt, wt, ht = cv2.boundingRect(cnt)
                        if((wt != 0 and ht != 0 and wt / ht > 0.3) and (ht / wt) > 0.3):
                            x = xt
                            y = yt
                            w = wt
                            h = ht
                        #cv2.drawContours(image_bgr, cnt, -1, (127,127,127), 15)
                            
                if(tmpArea > 0):
                    color = sortByColor(image_bgr[y:y+h,x:x+w])
                    cv2.rectangle(image_bgr, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    #roi = cropped[int(y):int(y + h), int(x):int(x+w)]

                cv2.putText(image_bgr, color, (5,50), 0, 1, (255,255,255), 2)
                cv2.imshow("frame", croppedBlur)
                #cv2.imshow("frame2", mask)
                #cv2.imshow("frame3", roi)

                if cv2.waitKey(1) == ord('q'):
                    cv2.imwrite("ItemDetectColor3.jpg", cropped)
                    break
            
        except Exception as e:
            
            print(e)
            print("There has been an error with the program. Exiting...")

        finally:
            # closing all open windows
            cv2.destroyAllWindows()

    #----------SHAPE AND SIZE----------
    elif(mode == 2):
        #Initialize camera
        try:
            picam2 = Picamera2()
            config = picam2.create_video_configuration({'size':(1600,720)})
            picam2.align_configuration(config)
            picam2.configure(config)
            picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition":9})#, 'LensPosition': 10})
            picam2.start()
            time.sleep(1)
        except:
            print("Unable to start camera. Exiting...")
            exit()

        try:
            while True:
                #Capture a frame from the camera
                array = picam2.capture_array("main")
                #print("Here")

                image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

                height = image_bgr.shape[0]
                width = image_bgr.shape[1]

                cropped = image_bgr#[int(height/4):int(3*height/4), int(width/4):int(3*width/4)]
                croppedGray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                croppedBlur = cv2.GaussianBlur(croppedGray, (5,5), 0)

                #mask = objectDetector.apply(cropped)
                _, mask = cv2.threshold(croppedBlur, 170, 255, cv2.THRESH_BINARY)

                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                x = 0
                y = 0
                w = 0
                h = 0
                #roi = cropped
                detectedShape = "?"
                detectedSize = 0

                tmpArea = -1
                shapeCont = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if(area > tmpArea and area > 3000):
                        xt, yt, wt, ht = cv2.boundingRect(cnt)
                        if((wt != 0 and ht != 0 and wt / ht > 0.4) and (ht / wt) > 0.4):
                            tmpArea = area
                            x = xt
                            y = yt
                            w = wt
                            h = ht
                            shapeCont = cnt
                        #cv2.drawContours(image_bgr, cnt, -1, (127,127,127), 15)
                            
                if(tmpArea > 0):
                    yStart = y - 20
                    yEnd = y + h + 20
                    xStart = x - 20
                    xEnd = x + w + 20
                    if(yStart > 0 and yEnd < height and xStart > 0 and xEnd < width):    
                        detectedShape = sortByShapeSize(image_bgr, shapeCont)
                        cv2.drawContours(image_bgr, shapeCont, -1, (0,255,0), 2)
                        cv2.rectangle(image_bgr, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    #roi = cropped[int(y):int(y + h), int(x):int(x+w)]

                cv2.putText(image_bgr, detectedShape, (5,50), 0, 1, (255,255,255), 2)
                cv2.imshow("frame", image_bgr)
                #cv2.imshow("frame2", mask)
                #cv2.imshow("frame3", roi)

                if cv2.waitKey(1) == ord('q'):
                    cv2.imwrite("ItemDetectColor3.jpg", cropped)
                    break
                
        except Exception as e:
            
            print(e)
            print("There has been an error with the program. Exiting...")

        finally:
            # closing all open windows
            cv2.destroyAllWindows()

    #----------OCR FOR LOOP----------
    elif(mode == 3):
        #Initialize camera
        try:
            picam2 = Picamera2()
            config = picam2.create_video_configuration({'size':(1600,720)})
            picam2.align_configuration(config)
            picam2.configure(config)
            picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition":9})#, 'LensPosition': 10})
            picam2.start()
            time.sleep(1)
        except:
            print("Unable to start camera. Exiting...")
            exit()

        try:
            validText = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            with PyTessBaseAPI(psm=10) as api:
                api.SetVariable('tessedit_char_whitelist', validText)
                while True:
                    #Capture a frame from the camera
                    array = picam2.capture_array("main")
                    #print("Here")

                    image_bgr = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

                    height = image_bgr.shape[0]
                    width = image_bgr.shape[1]

                    cropped = image_bgr#[int(height/4):int(3*height/4), int(width/4):int(3*width/4)]
                    croppedGray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                    croppedBlur = cv2.GaussianBlur(croppedGray, (5,5), 0)

                    #mask = objectDetector.apply(cropped)
                    _, mask = cv2.threshold(croppedBlur, 127, 255, cv2.THRESH_BINARY)

                    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    x = 0
                    y = 0
                    w = 0
                    h = 0
                    #roi = cropped
                    character = "?"

                    tmpArea = -1
                    for cnt in contours:
                        area = cv2.contourArea(cnt)
                        if(area > tmpArea and area > 3000):
                            tmpArea = area
                            xt, yt, wt, ht = cv2.boundingRect(cnt)
                            if((wt != 0 and ht != 0 and wt / ht > 0.4) and (ht / wt) > 0.4):
                                x = xt
                                y = yt
                                w = wt
                                h = ht
                            #cv2.drawContours(image_bgr, cnt, -1, (127,127,127), 15)
                                
                    if(tmpArea > 0):
                        yStart = y - 20
                        yEnd = y + h + 20
                        xStart = x - 20
                        xEnd = x + w + 20
                        if(yStart > 0 and yEnd < height and xStart > 0 and xEnd < width):    
                            chars = {}
                            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
                            croppedRGB = image_rgb[yStart:yEnd,xStart:xEnd]
                            # rotHeight, rotWidth = croppedRGB.shape[:2]
                            # center = (rotWidth / 2, rotHeight / 2)
                            # degree = -180
                            # while(degree < 180):
                            #     rotationMatrix = cv2.getRotationMatrix2D(center = center, angle = degree, scale = 1)
                            #     rotatedImage = cv2.warpAffine(croppedRGB, rotationMatrix, (width, height))
                            #     character = sortByOCR(rotatedImage, api)[0]
                            #     if(character in chars):
                            #         chars[character] = chars[character] + 2
                            #     else:
                            #         chars[character] = 2
                            #     degree = degree + 90
                            character = sortByOCR(croppedRGB, api)[0]
                            if(character in chars):
                                chars[character] = chars[character] + 2
                            else:
                                chars[character] = 2
                            character = sortByOCR(cv2.rotate(croppedRGB, cv2.ROTATE_90_COUNTERCLOCKWISE), api)[0]
                            if(character in chars):
                                chars[character] = chars[character] + 2
                            else:
                                chars[character] = 2
                            character = sortByOCR(cv2.rotate(croppedRGB, cv2.ROTATE_180), api)[0]
                            if(character in chars):
                                chars[character] = chars[character] + 2
                            else:
                                chars[character] = 2
                            character = sortByOCR(cv2.rotate(croppedRGB, cv2.ROTATE_90_CLOCKWISE), api)[0]
                            if(character in chars):
                                chars[character] = chars[character] + 2
                            else:
                                chars[character] = 2
                            cv2.rectangle(image_bgr, (x, y), (x + w, y + h), (0, 0, 255), 3)
                            chars["?"] = 1
                            character = max(chars, key=chars.get)
                        #roi = cropped[int(y):int(y + h), int(x):int(x+w)]

                    cv2.putText(image_bgr, character, (5,50), 0, 1, (255,255,255), 2)
                    cv2.imshow("frame", image_bgr)
                    #cv2.imshow("frame2", mask)
                    #cv2.imshow("frame3", roi)

                    if cv2.waitKey(1) == ord('q'):
                        cv2.imwrite("ItemDetectColor3.jpg", cropped)
                        break
                
        except Exception as e:
            
            print(e)
            print("There has been an error with the program. Exiting...")

        finally:
            # closing all open windows
            cv2.destroyAllWindows()

    cv2.destroyAllWindows()


