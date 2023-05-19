#Import libraries
import RPi.GPIO as GPIO          
from time import sleep
import time
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

#----------COLOR SORTING FUNCTION DEFINITION----------
def sortByColor(image):
    height1, width1, channels = image.shape
    returnVal = [1, "Default"]
    bin = 1
    if(height1 == 0 or width1 == 0):
        #return default
        return returnVal
    cropHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    
    testPixel = cropHSV[int((height1)/2), int((width1)/2)]
    hueValue = testPixel[0]
        
    if(hueValue < 10):
        color = 'Red'
        bin = 2
    elif (hueValue < 25):
        color = 'Orange'
        bin = 3
    elif (hueValue < 30):
        color = 'Yellow'
        bin = 4
    elif(hueValue < 45):
        color = 'Light Green'
        bin = 5
    elif(hueValue < 60):
        color = 'Light Green'
        bin = 5
    elif(hueValue < 90):
        color = 'Green'
        bin = 5
    elif(hueValue < 100):
        color = 'Cyan'
        bin = 6
    elif(hueValue < 135):
        color = 'Blue'
        bin = 6
    elif(hueValue < 150):
        color = 'Purple'
        bin = 7
    elif(hueValue < 165):
        color = 'Magenta'
        bin = 7
    elif(hueValue < 176):
        color = 'Pink'
        bin = 8
    elif(hueValue < 181):
        color = "Red"
        bin = 2
    
    saturation = testPixel[1]
    if(saturation < 2):
        color = 'White'
        bin = 9

    
    value = testPixel[2]
    if(value < 55):
        color = 'Black'
        bin = 1

    returnVal[0] = bin
    returnVal[1] = color

    return(returnVal)


#----------Shape/Size SORTING FUNCTION DEFINITION----------
def sortByShapeSize(image, contour):
    height1, width1, channels = image.shape
    shape = "?"
    returnVal = [1, "?"]
    bin = 1
    if(height1 == 0 or width1 == 0):
        return returnVal
    approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

    #cv2.drawContours(cropped, cnt2, -1, (255,255,255), 5)
    #time.sleep(0.10)
    print(len(approx))
    if len(approx) == 3:
        shape = "Triangle"
        bin = 3
    elif len(approx) == 4:
        if(height1 / width1 < 0.8 or width1 / height1 < 0.8):
            shape = "Rectangle"
            bin = 4
        else:
            shape = "Square"
            bin = 2
    elif len(approx) == 5:
        shape = "Pentagon"
        bin = 5
    elif len(approx) == 6:
        shape = "Hexagon"
        bin = 6
    elif len(approx) == 7:
        shape = "Heptagon"
        bin = 7
    elif len(approx) == 8:
        shape = "Octagon"
        bin = 8
    elif len(approx) == 9:
        shape = "Nonagon"
        bin = 9
    elif len(approx) == 10:
        shape = "Star"
        bin = 10
    if len(approx) > 11:
        shape = "Circle"
        bin = 11
    #shape = shape + "," + str(len(approx))
    #time.sleep(0.10)
    #shape = shape + ', ' + str(valueInMM)
    returnVal[0] = bin
    returnVal[1] = shape
    return returnVal


#----------OCR SORTING FUNCTION DEFINITION----------
def sortByOCR(image, api):
    height1, width1, channels = image.shape
    readCharacter = "?"
    bin = 1
    returnVal = [1, "?"]
    if(height1 == 0 or width1 == 0):
        return returnVal
    imPil = Image.fromarray(image)

    api.SetImage(imPil)
    conf = api.MeanTextConf()
    if (conf > 40):
        readCharacter = api.GetUTF8Text()[0]
    returnVal[1] = readCharacter
    if(readCharacter != "?"):
        returnVal[0] = ord(readCharacter) % 12 + 1
    return returnVal

#STORAGE fILE INITIALIZATION
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


#GPIO and Variable Assignmments
#in and en variables represent pins, while pos and timer are software variables
GPIO.cleanup()
#ACTUATOR 1
act1in1 = 27
act1in2 =17
act1pos = 0
act1timer = 0
act1on = False
act1delay = 0.15
#ACTUATOR 2
act2in1 = 11
act2in2 = 10
act2pos = 0
act2timer = 0
act2on = False
act2delay = 0.18
#ACTUATOR 3
act3in1 = 19
act3in2 = 26
act3pos = 0
act3timer = 0
act3on = False
act3delay = 0.15
#ACTUATOR 4
act4in1 = 14
act4in2 = 15
act4pos = 0
act4timer = 0
act4on = False
act4delay = 0.15
#ACTUATOR 5
act5in1 = 23
act5in2 = 24
act5pos = 0
act5timer = 0
act5on = False
act5delay = 0.15
#ACTUATOR 6
act6in1 = 20
act6in2 = 21
act6pos = 0
act6timer = 0
act6on = False
act6delay = 0.15

#Rotating entryway motor on funnel

#Top Motor
topMotorIn1 = 22

#Bottom motor
bottomMotorIn1 = 13
temp1=1

#Rotation Motor
rotPWM = 16
rotIn1 = 12
rotIn2 = 1



#Debug variable, will be removed in a bit
temp1=1


print("Initializing GPIO...")
#GPIO LIBRARY INITIALIZATION
#INITIALIZE ALL PINS FOR OUTPUT AND SET THEM TO LOW
GPIO.setmode(GPIO.BCM)
#ACTUATOR 1 INITIALIZATION
GPIO.setup(act1in1, GPIO.OUT)
GPIO.setup(act1in2, GPIO.OUT)
GPIO.output(act1in1, GPIO.LOW)
GPIO.output(act1in2, GPIO.LOW)
#ACTUATOR 2 INITIALIZATION
GPIO.setup(act2in1, GPIO.OUT)
GPIO.setup(act2in2, GPIO.OUT)
GPIO.output(act2in1, GPIO.LOW)
GPIO.output(act2in2, GPIO.LOW)
#ACTUATOR 3 INITIALIZATION
GPIO.setup(act3in1, GPIO.OUT)
GPIO.setup(act3in2, GPIO.OUT)
GPIO.output(act3in1, GPIO.LOW)
GPIO.output(act3in2, GPIO.LOW)
#ACTUATOR 4 INITIALIZATION
GPIO.setup(act4in1, GPIO.OUT)
GPIO.setup(act4in2, GPIO.OUT)
GPIO.output(act4in1, GPIO.LOW)
GPIO.output(act4in2, GPIO.LOW)
#ACTUATOR 5 INITIALIZATION
GPIO.setup(act5in1, GPIO.OUT)
GPIO.setup(act5in2, GPIO.OUT)
GPIO.output(act5in1, GPIO.LOW)
GPIO.output(act5in2, GPIO.LOW)
#ACTUATOR 6 INITIALIZATION
GPIO.setup(act6in1, GPIO.OUT)
GPIO.setup(act6in2, GPIO.OUT)
GPIO.output(act6in1, GPIO.LOW)
GPIO.output(act6in2, GPIO.LOW)

#Top Motor
GPIO.setup(topMotorIn1,GPIO.OUT)
pTop=GPIO.PWM(topMotorIn1,5)
#pTop.start(35)

#Bottom Motor
GPIO.setup(bottomMotorIn1,GPIO.OUT)
pBottom=GPIO.PWM(bottomMotorIn1,18)
pBottom.start(20)

#Top spinning thing
GPIO.setup(rotPWM, GPIO.OUT)
GPIO.setup(rotIn1, GPIO.OUT)
GPIO.setup(rotIn2, GPIO.LOW)
pRotor = GPIO.PWM(rotPWM, 10000)
GPIO.output(rotIn1, GPIO.HIGH)
GPIO.output(rotIn2, GPIO.LOW)
pRotor.start(25)
rotorDirection = 1
rotorTimer = time.time() + 1

#Top Rotor initialization

#ACTUATOR CALIBRATION
print("GPIO set!")
print("Calibrating actuators by moving them to the left...")
#Actuator1
GPIO.output(act1in1, GPIO.HIGH)
GPIO.output(act1in2, GPIO.LOW)
#Actuator2
GPIO.output(act2in1, GPIO.HIGH)
GPIO.output(act2in2, GPIO.LOW)
#Actuator3
GPIO.output(act3in1, GPIO.HIGH)
GPIO.output(act3in2, GPIO.LOW)
#Actuator4
GPIO.output(act4in1, GPIO.HIGH)
GPIO.output(act4in2, GPIO.LOW)
#Actuator5
GPIO.output(act5in1, GPIO.HIGH)
GPIO.output(act5in2, GPIO.LOW)
#Actuator6
GPIO.output(act6in1, GPIO.HIGH)
GPIO.output(act6in2, GPIO.LOW)

#Leaving the configuration on for 1 second
tempTime = time.time()
while((tempTime + 1) > time.time()):
    x = 1 # Placeholder

#Reset all of them to low
#Actuator1
GPIO.output(act1in1, GPIO.LOW)
GPIO.output(act1in2, GPIO.LOW)
#Actuator2
GPIO.output(act2in1, GPIO.LOW)
GPIO.output(act2in2, GPIO.LOW)
#Actuator3
GPIO.output(act3in1, GPIO.LOW)
GPIO.output(act3in2, GPIO.LOW)
#Actuator4
GPIO.output(act4in1, GPIO.LOW)
GPIO.output(act4in2, GPIO.LOW)
#Actuator5
GPIO.output(act5in1, GPIO.LOW)
GPIO.output(act5in2, GPIO.LOW)
#Actuator6
GPIO.output(act6in1, GPIO.LOW)
GPIO.output(act6in2, GPIO.LOW)

#--------------------------Actuator Function Definitions-------------------------

#BASIC ACTUATOR CONTROLS
#Actuator 1
def turnOffAct1():
    GPIO.output(act1in1,GPIO.LOW)
    GPIO.output(act1in2,GPIO.LOW)

def moveAct1Left():
    GPIO.output(act1in1,GPIO.HIGH)
    GPIO.output(act1in2,GPIO.LOW)

def moveAct1Right():
    GPIO.output(act1in1,GPIO.LOW)
    GPIO.output(act1in2,GPIO.HIGH)

#Actuator 2
def turnOffAct2():
    GPIO.output(act2in1,GPIO.LOW)
    GPIO.output(act2in2,GPIO.LOW)

def moveAct2Left():
    GPIO.output(act2in1,GPIO.HIGH)
    GPIO.output(act2in2,GPIO.LOW)

def moveAct2Right():
    GPIO.output(act2in1,GPIO.LOW)
    GPIO.output(act2in2,GPIO.HIGH)

#Actuator 3
def turnOffAct3():
    GPIO.output(act3in1,GPIO.LOW)
    GPIO.output(act3in2,GPIO.LOW)

def moveAct3Left():
    GPIO.output(act3in1,GPIO.HIGH)
    GPIO.output(act3in2,GPIO.LOW)

def moveAct3Right():
    GPIO.output(act3in1,GPIO.LOW)
    GPIO.output(act3in2,GPIO.HIGH)

#Actuator 4
def turnOffAct4():
    GPIO.output(act4in1,GPIO.LOW)
    GPIO.output(act4in2,GPIO.LOW)

def moveAct4Left():
    GPIO.output(act4in1,GPIO.HIGH)
    GPIO.output(act4in2,GPIO.LOW)

def moveAct4Right():
    GPIO.output(act4in1,GPIO.LOW)
    GPIO.output(act4in2,GPIO.HIGH)

#Actuator 5
def turnOffAct5():
    GPIO.output(act5in1,GPIO.LOW)
    GPIO.output(act5in2,GPIO.LOW)

def moveAct5Left():
    GPIO.output(act5in1,GPIO.HIGH)
    GPIO.output(act5in2,GPIO.LOW)

def moveAct5Right():
    GPIO.output(act5in1,GPIO.LOW)
    GPIO.output(act5in2,GPIO.HIGH)

#Actuator 6
def turnOffAct6():
    GPIO.output(act6in1,GPIO.LOW)
    GPIO.output(act6in2,GPIO.LOW)

def moveAct6Left():
    GPIO.output(act6in1,GPIO.HIGH)
    GPIO.output(act6in2,GPIO.LOW)

def moveAct6Right():
    GPIO.output(act6in1,GPIO.LOW)
    GPIO.output(act6in2,GPIO.HIGH)




#ACTUATOR FUNCTION DEFINITION
#This function takes as an input a bin number, and moves the actuators accordingly
#Bin numbers go as follows:
# 1  2
# 3  4
# 5  6
# 7  8
# 9  10
# 11 12
def moveActuators(binNumber):
    left = 0
    middle = 1
    right = 2

    returnSum = 0

    global act1in1
    global act1in2
    global act1pos
    global act1timer
    global act1on
    global act1delay
    #ACTUATOR 2
    global act2in1
    global act2in2
    global act2pos
    global act2timer
    global act2on
    global act2delay
    #ACTUATOR 3
    global act3in1
    global act3in2
    global act3pos
    global act3timer
    global act3on
    global act3delay
    #ACTUATOR 4
    global act4in1
    global act4in2
    global act4pos
    global act4timer
    global act4on
    global act4delay
    #ACTUATOR 5
    global act5in1
    global act5in2
    global act5pos
    global act5timer
    global act5on
    global act5delay
    #ACTUATOR 6
    global act6in1
    global act6in2
    global act6pos
    global act6timer
    global act6on
    global act6delay
    #print(act1pos)
    #The higher the bin level, the more actuators we need to move
    #Want to make more common values be bins 1,2,3,4 etc
    if(binNumber == 1):
        #Move act1 to right only if its not doing any current movement and not in position already
        if(act1pos != right):
            if(not act1on):
                moveAct1Right()
                act1on = True
                if(act1pos == 0):
                    act1timer = time.time() + act1delay * 2
                else:
                    act1timer = time.time() + act1delay
                act1pos = right
    
    elif(binNumber == 2):
        #Move act1 to left only if its not doing any current movement and not in position already
        if(act1pos != left):
            if(not act1on):
                moveAct1Left()
                act1on = True
                if(act1pos == 2):
                    act1timer = time.time() + act1delay * 2
                else:
                    act1timer = time.time() + act1delay
                act1pos = left
    
    elif(binNumber == 3):
        #Move act1 to middle
        if(act1pos == left):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        elif(act1pos == right):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        #Move act2 to right only if its not doing any current movement and not in position already
        if(act2pos != right):
            if(not act2on):
                moveAct2Right()
                act2on = True
                if(act2pos == 0):
                    act2timer = time.time() + act2delay * 2
                else:
                    act2timer = time.time() + act2delay
                act2pos = right   
    
    elif(binNumber == 4):
        #Move act1 to middle
        if(act1pos == left):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        elif(act1pos == right):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        #Move act2 to left only if its not doing any current movement and not in position already
        if(act2pos != left):
            if(not act2on):
                moveAct2Left()
                act2on = True
                if(act2pos == 2):
                    act2timer = time.time() + act2delay * 2
                else:
                    act2timer = time.time() + act2delay
                act2pos = left

    elif(binNumber == 5):
        #Move act1 to middle
        if(act1pos == left):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        elif(act1pos == right):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        #Move act2 to middle
        if(act2pos == left):
            if(not act2on):
                moveAct2Right()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        elif(act2pos == right):
            if(not act2on):
                moveAct2Left()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        #Move act 3 to right
        if(act3pos != right):
            if(not act3on):
                moveAct3Right()
                act3on = True
                if(act3pos == left):
                    act3timer = time.time() + act3delay * 2
                else:
                    act3timer = time.time() + act3delay
                act3pos = right  

    elif(binNumber == 6):
        #Move act1 to middle
        if(act1pos == left):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        elif(act1pos == right):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        #Move act2 to middle
        if(act2pos == left):
            if(not act2on):
                moveAct2Right()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        elif(act2pos == right):
            if(not act2on):
                moveAct2Left()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        #Move act 3 to left
        if(act3pos != left):
            if(not act3on):
                moveAct3Left()
                act3on = True
                if(act3pos == right):
                    act3timer = time.time() + act3delay * 2
                else:
                    act3timer = time.time() + act3delay
                act3pos = left
    
    elif(binNumber == 7):
        #Move act1 to middle
        if(act1pos == left):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        elif(act1pos == right):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        #Move act2 to middle
        if(act2pos == left):
            if(not act2on):
                moveAct2Right()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        elif(act2pos == right):
            if(not act2on):
                moveAct2Left()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        #Move act 3 to middle
        if(act3pos == left):
            if(not act3on):
                moveAct3Right()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        elif(act3pos == right):
            if(not act3on):
                moveAct3Left()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        #Move act 4 to right
        if(act4pos != right):
            if(not act4on):
                moveAct4Right()
                act4on = True
                if(act4pos == left):
                    act4timer = time.time() + act4delay * 2
                else:
                    act4timer = time.time() + act4delay
                act4pos = right
    
    elif(binNumber == 8):
        #Move act1 to middle
        if(act1pos == left):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        elif(act1pos == right):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        #Move act2 to middle
        if(act2pos == left):
            if(not act2on):
                moveAct2Right()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        elif(act2pos == right):
            if(not act2on):
                moveAct2Left()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        #Move act 3 to middle
        if(act3pos == left):
            if(not act3on):
                moveAct3Right()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        elif(act3pos == right):
            if(not act3on):
                moveAct3Left()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        #Move act 4 to left
        if(act4pos != left):
            if(not act4on):
                moveAct4Left()
                act4on = True
                if(act4pos == right):
                    act4timer = time.time() + act4delay * 2
                else:
                    act4timer = time.time() + act4delay
                act4pos = left
        
    elif(binNumber == 9):
        #Move act1 to middle
        if(act1pos == left):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        elif(act1pos == right):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        #Move act2 to middle
        if(act2pos == left):
            if(not act2on):
                moveAct2Right()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        elif(act2pos == right):
            if(not act2on):
                moveAct2Left()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        #Move act 3 to middle
        if(act3pos == left):
            if(not act3on):
                moveAct3Right()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        elif(act3pos == right):
            if(not act3on):
                moveAct3Left()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        #Move act 4 to middle
        if(act4pos == left):
            if(not act4on):
                moveAct4Right()
                act4on = True
                act4timer = time.time() + act4delay
                act4pos = middle
        elif(act4pos == right):
            if(not act4on):
                moveAct4Left()
                act4on = True
                act4timer = time.time() + act4delay
                act4pos = middle
        #Move act 5 to right
        if(act5pos != right):
            if(not act5on):
                moveAct5Right()
                act5on = True
                if(act5pos == left):
                    act5timer = time.time() + act5delay * 2
                else:
                    act5timer = time.time() + act5delay
                act5pos = right
    
    elif(binNumber == 10):
        #Move act1 to middle
        if(act1pos == left):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        elif(act1pos == right):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        #Move act2 to middle
        if(act2pos == left):
            if(not act2on):
                moveAct2Right()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        elif(act2pos == right):
            if(not act2on):
                moveAct2Left()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        #Move act 3 to middle
        if(act3pos == left):
            if(not act3on):
                moveAct3Right()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        elif(act3pos == right):
            if(not act3on):
                moveAct3Left()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        #Move act 4 to middle
        if(act4pos == left):
            if(not act4on):
                moveAct4Right()
                act4on = True
                act4timer = time.time() + act4delay
                act4pos = middle
        elif(act4pos == right):
            if(not act4on):
                moveAct4Left()
                act4on = True
                act4timer = time.time() + act4delay
                act4pos = middle
        #Move act 5 to left
        if(act5pos != left):
            if(not act5on):
                moveAct5Left()
                act5on = True
                if(act5pos == right):
                    act5timer = time.time() + act5delay * 2
                else:
                    act5timer = time.time() + act5delay
                act5pos = left
    
    elif(binNumber == 11):
        #Move act1 to middle
        if(act1pos == left):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        elif(act1pos == right):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        #Move act2 to middle
        if(act2pos == left):
            if(not act2on):
                moveAct2Right()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        elif(act2pos == right):
            if(not act2on):
                moveAct2Left()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        #Move act 3 to middle
        if(act3pos == left):
            if(not act3on):
                moveAct3Right()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        elif(act3pos == right):
            if(not act3on):
                moveAct3Left()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        #Move act 4 to middle
        if(act4pos == left):
            if(not act4on):
                moveAct4Right()
                act4on = True
                act4timer = time.time() + act4delay
                act4pos = middle
        elif(act4pos == right):
            if(not act4on):
                moveAct4Left()
                act4on = True
                act4timer = time.time() + act4delay
                act4pos = middle
        #Move act 5 to middle
        if(act5pos == left):
            if(not act5on):
                moveAct5Right()
                act5on = True
                act5timer = time.time() + act5delay
                act5pos = middle
        elif(act5pos == right):
            if(not act5on):
                moveAct5Left()
                act5on = True
                act5timer = time.time() + act5delay
                act5pos = middle
        #Move act 6 to right
        if(act6pos != right):
            if(not act6on):
                moveAct6Right()
                act6on = True
                if(act6pos == left):
                    act6timer = time.time() + act6delay * 2
                else:
                    act6timer = time.time() + act6delay
                act6pos = right
    
    elif(binNumber == 12):
        #Move act1 to middle
        if(act1pos == left):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        elif(act1pos == right):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = middle
        #Move act2 to middle
        if(act2pos == left):
            if(not act2on):
                moveAct2Right()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        elif(act2pos == right):
            if(not act2on):
                moveAct2Left()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = middle
        #Move act 3 to middle
        if(act3pos == left):
            if(not act3on):
                moveAct3Right()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        elif(act3pos == right):
            if(not act3on):
                moveAct3Left()
                act3on = True
                act3timer = time.time() + act3delay
                act3pos = middle
        #Move act 4 to middle
        if(act4pos == left):
            if(not act4on):
                moveAct4Right()
                act4on = True
                act4timer = time.time() + act4delay
                act4pos = middle
        elif(act4pos == right):
            if(not act4on):
                moveAct4Left()
                act4on = True
                act4timer = time.time() + act4delay
                act4pos = middle
        #Move act 5 to middle
        if(act5pos == left):
            if(not act5on):
                moveAct5Right()
                act5on = True
                act5timer = time.time() + act5delay
                act5pos = middle
        elif(act5pos == right):
            if(not act5on):
                moveAct5Left()
                act5on = True
                act5timer = time.time() + act5delay
                act5pos = middle
        #Move act 6 to left
        if(act6pos != left):
            if(not act6on):
                moveAct6Left()
                act6on = True
                if(act6pos == right):
                    act6timer = time.time() + act6delay * 2
                else:
                    act6timer = time.time() + act6delay
                act6pos = left

    
    #Turn off actuators that have reachd their time limit
    if(act1timer < time.time()):
        turnOffAct1()
        act1on = False
        returnSum = returnSum + 1
    if(act2timer < time.time()):
        turnOffAct2()
        act2on = False
        returnSum = returnSum + 1
    if(act3timer < time.time()):
        turnOffAct3()
        act3on = False
        returnSum = returnSum + 1
    if(act4timer < time.time()):
        turnOffAct4()
        act4on = False
        returnSum = returnSum + 1
    if(act5timer < time.time()):
        turnOffAct5()
        act5on = False
        returnSum = returnSum + 1
    if(act6timer < time.time()):
        turnOffAct6()
        act6on = False
        returnSum = returnSum + 1

    if returnSum < 6:
        return True
    else:
        return False

with open(outputFileFullPath, "w") as outputFile:
    #Sample input for mode selection
    mode = int(input("Please enter your sorting mode.\n1: Color\n2: Shape/Size\n3: OCR\nAnswer: ").strip())

    fileResults = {}

    #----------COLOR FOR LOOP----------
    #Configure pre-set values that change between modes
    if(mode == 1):
        #Initialize camera
        try:
            picam2 = Picamera2()
            config = picam2.create_video_configuration()
            picam2.align_configuration(config)
            picam2.configure(config)
            picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition":9999})#, 'LensPosition': 10})
            picam2.start()
            time.sleep(1)
        except:
            print("Unable to start camera. Exiting...")
            exit()

        #Hash map keeping track of return Values
        binMap = {1:1}
        colorMap = {"Default":1}
        #mapTimer = time.time()
        detected = False

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
                _, mask = cv2.threshold(croppedBlur, 65, 255, cv2.THRESH_BINARY)

                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                x = 0
                y = 0
                w = 0
                h = 0
                #roi = cropped
                color = "Default"
                binNum = 1
                tempDetected = False

                tmpArea = -1
                contourId = 0
                for cnt in contours:
                    if contourId == 0:
                        contourId = 1
                        continue
                    area = cv2.contourArea(cnt)
                    if((area > tmpArea) and (area > 15000)):
                        tmpArea = area
                        xt, yt, wt, ht = cv2.boundingRect(cnt)
                        if(((wt - x > 20) and (ht - y > 20) and wt / ht > 0.6) and (ht / wt) > 0.6):
                            x = xt
                            y = yt
                            w = wt
                            h = ht
                        #cv2.drawContours(image_bgr, cnt, -1, (127,127,127), 15)
                            
                if(tmpArea > 15000) and x > 5 and y > 5:
                    #color = sortByColor(image_bgr[y:y+h,x:x+w])
                    functionReturn = sortByColor(image_bgr[y:y+h,x:x+w])
                    binNum = functionReturn[0]
                    color = functionReturn[1]
                    if not (binNum in binMap):
                       binMap[binNum] = 0
                    binMap[binNum] = binMap[binNum] + 1
                    if not (color in colorMap):
                       colorMap[color] = 0
                    colorMap[color] = colorMap[color] + 1

                    detected = True
                    tempDetected = True
                    cv2.rectangle(image_bgr, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    #roi = cropped[int(y):int(y + h), int(x):int(x+w)]

                colorMap["Default"] = 1
                colorOut = max(colorMap, key=colorMap.get)
                
                #Item has left the frame
                if(detected == True and tempDetected == False):
                    detected = False
                    outBin = max(binMap, key=binMap.get)
                    print(outBin)
                    outVal = max(colorMap, key=colorMap.get)

                    if(not (outVal in fileResults)):
                        fileResults[outVal] = 0
                    fileResults[outVal] = fileResults[outVal] + 1

                    while moveActuators(outBin):
                        dummy = 1
                    for key, value in colorMap.items():
                        colorMap[key] = 0
                    colorMap["Default"] = 1
                    for key, value in binMap.items():
                        binMap[key] = 0
                    binMap[1] = 1
                    #mapTimer = time.time() + 1

                cv2.putText(image_bgr, colorOut, (5,50), 0, 1, (255,255,255), 2)
                cv2.imshow("frame", image_bgr)
                #cv2.imshow("frame2", mask)
                #cv2.imshow("frame3", roi)

                if cv2.waitKey(1) == ord('q'):
                    #cv2.imwrite("ItemDetectColor3.jpg", cropped)
                    jsonObject = json.dumps(fileResults, indent=4)
                    outputFile.write(jsonObject)
                    break
                if(rotorTimer < time.time()):
                    rotorTimer = time.time() + 1
                    if (rotorDirection == 1):
                        GPIO.output(rotIn1, GPIO.LOW)
                        GPIO.output(rotIn2, GPIO.HIGH)
                        rotorDirection = 2
                    else:
                        GPIO.output(rotIn1, GPIO.HIGH)
                        GPIO.output(rotIn2, GPIO.LOW)
                        rotorDirection = 1
            
        except Exception as e:
            
            print(e)
            print("There has been an error with the program. Exiting...")

        finally:
            # closing all open windows
            cv2.destroyAllWindows()
            GPIO.cleanup()


    #----------SHAPE AND SIZE----------
    elif(mode == 2):
        #Initialize camera
        try:
            picam2 = Picamera2()
            config = picam2.create_video_configuration({'size':(1600,720)})
            picam2.align_configuration(config)
            picam2.configure(config)
            picam2.set_controls({'AfMode': controls.AfModeEnum.Manual, "LensPosition":12})#, 'LensPosition': 10})
            picam2.start()
            time.sleep(1)
        except:
            print("Unable to start camera. Exiting...")
            exit()

        #Hash map keeping track of return Values
        binMap = {1:1}
        shapeMap = {"?":1}
        #mapTimer = time.time()
        detected = False

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
                _, mask = cv2.threshold(croppedBlur, 65, 255, cv2.THRESH_BINARY)

                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                x = 0
                y = 0
                w = 0
                h = 0
                #roi = cropped
                
                detectedShape = "?"
                detectedSize = 0

                binNum = 1
                tempDetected = False

                tmpArea = -1
                shapeCont = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if(area > tmpArea and area > 15000):
                        xt, yt, wt, ht = cv2.boundingRect(cnt)
                        if((wt != 0 and ht != 0 and wt / ht > 0.6) and (ht / wt) > 0.6):
                            tmpArea = area
                            x = xt
                            y = yt
                            w = wt
                            h = ht
                            shapeCont = cnt
                        #cv2.drawContours(image_bgr, cnt, -1, (127,127,127), 15)
                            
                if(tmpArea > 0 and x > 5 and y > 5):
                    yStart = y - 10
                    yEnd = y + h + 10
                    xStart = x - 10
                    xEnd = x + w + 10
                    if(yStart > 0 and yEnd < height and xStart > 0 and xEnd < width):    
                        functionReturn = sortByShapeSize(image_bgr[yStart:yEnd,xStart:xEnd], shapeCont)

                        binNum = functionReturn[0]
                        shape = functionReturn[1]
                        if not (binNum in binMap):
                            binMap[binNum] = 0
                        binMap[binNum] = binMap[binNum] + 1
                        if not (shape in shapeMap):
                            shapeMap[shape] = 0
                        shapeMap[shape] = shapeMap[shape] + 1

                        detected = True
                        tempDetected = True
                        cv2.drawContours(image_bgr, shapeCont, -1, (0,255,0), 2)
                        cv2.rectangle(image_bgr, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    #roi = cropped[int(y):int(y + h), int(x):int(x+w)]

                
                shapeMap["Default"] = 1
                shapeOut = max(shapeMap, key=shapeMap.get)

                #Item has left the frame
                if(detected == True and tempDetected == False):
                    detected = False
                    outBin = max(binMap, key=binMap.get)
                    print(outBin)
                    outVal = max(shapeMap, key=shapeMap.get)

                    if(not (outVal in fileResults)):
                        fileResults[outVal] = 0
                    fileResults[outVal] = fileResults[outVal] + 1

                    while moveActuators(outBin):
                        dummy = 1
                    for key, value in shapeMap.items():
                        shapeMap[key] = 0
                    shapeMap["?"] = 1
                    for key, value in binMap.items():
                        binMap[key] = 0
                    binMap[1] = 1
                    #mapTimer = time.time() + 1
                
                cv2.putText(image_bgr, shapeOut, (5,50), 0, 1, (255,255,255), 2)
                cv2.imshow("frame", image_bgr)
                #cv2.imshow("frame2", mask)
                #cv2.imshow("frame3", roi)

                if cv2.waitKey(1) == ord('q'):
                    jsonObject = json.dumps(fileResults, indent=4)
                    outputFile.write(jsonObject)
                    break
                if(rotorTimer < time.time()):
                    rotorTimer = time.time() + 1
                    if (rotorDirection == 1):
                        GPIO.output(rotIn1, GPIO.LOW)
                        GPIO.output(rotIn2, GPIO.HIGH)
                        rotorDirection = 2
                    else:
                        GPIO.output(rotIn1, GPIO.HIGH)
                        GPIO.output(rotIn2, GPIO.LOW)
                        rotorDirection = 1
                
        except Exception as e:
            
            print(e)
            print("There has been an error with the program. Exiting...")

        finally:
            # closing all open windows
            cv2.destroyAllWindows()
            GPIO.cleanup()


    #----------OCR FOR LOOP----------
    elif(mode == 3):
        #Initialize camera
        try:
            picam2 = Picamera2()
            config = picam2.create_video_configuration({'size':(900,720)})
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
            binMap = {1:1}
            characterMap = {"?":1}
            detected = False
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
                    _, mask = cv2.threshold(croppedBlur, 65, 255, cv2.THRESH_BINARY)

                    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    x = 0
                    y = 0
                    w = 0
                    h = 0
                    #roi = cropped
                    character = "?"
                    binNum = 1
                    tempDetected = False

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
                                
                    if(tmpArea > 0 and x > 5 and y > 5):
                        detected = True
                        tempDetected = True
                        yStart = y - 10
                        yEnd = y + h + 10
                        xStart = x - 10
                        xEnd = x + w + 10
                        if(yStart > 0 and yEnd < height and xStart > 0 and xEnd < width):    
                            chars = {}
                            tempBins = {}
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
                            #We test rotations in 90-degree increments
                            #Much more easily fixable if the rotation stuff is moved to the function
                            
                            functionResult = sortByOCR(croppedRGB, api)
                            binNum = functionResult[0]
                            character = functionResult[1]
                            if(character in chars):
                                chars[character] = chars[character] + 2
                            else:
                                chars[character] = 2
                            if(not (binNum in tempBins)):
                                tempBins[binNum] = 0
                            tempBins[binNum] = tempBins[binNum] + 2

                            functionResult = sortByOCR(cv2.rotate(croppedRGB, cv2.ROTATE_90_COUNTERCLOCKWISE), api)
                            binNum = functionResult[0]
                            character = functionResult[1]
                            if(character in chars):
                                chars[character] = chars[character] + 2
                            else:
                                chars[character] = 2
                            if(not (binNum in tempBins)):
                                tempBins[binNum] = 0
                            tempBins[binNum] = tempBins[binNum] + 2

                            functionResult = sortByOCR(cv2.rotate(croppedRGB, cv2.ROTATE_180), api)
                            binNum = functionResult[0]
                            character = functionResult[1]
                            if(character in chars):
                                chars[character] = chars[character] + 2
                            else:
                                chars[character] = 2
                            if(not (binNum in tempBins)):
                                tempBins[binNum] = 0
                            tempBins[binNum] = tempBins[binNum] + 2

                            functionResult = sortByOCR(cv2.rotate(croppedRGB, cv2.ROTATE_90_CLOCKWISE), api)
                            binNum = functionResult[0]
                            character = functionResult[1]
                            if(character in chars):
                                chars[character] = chars[character] + 2
                            else:
                                chars[character] = 2
                            if(not (binNum in tempBins)):
                                tempBins[binNum] = 0
                            tempBins[binNum] = tempBins[binNum] + 2

                            cv2.rectangle(image_bgr, (x, y), (x + w, y + h), (0, 0, 255), 3)
                            chars["?"] = 1
                            tempBins[1] = 1
                            character = max(chars, key=chars.get)
                            if(not (character in characterMap)):
                                characterMap[character] = 0
                            characterMap[character] = characterMap[character] + 1
                            binNum = max(tempBins, key=tempBins.get)
                            if not (binNum in binMap):
                                binMap[binNum] = 0
                            binMap[binNum] = binMap[binNum] + 1
                            
                    
                        #roi = cropped[int(y):int(y + h), int(x):int(x+w)]
                    characterMap["?"] = 1
                    characterOut = max(characterMap, key=characterMap.get)
                    
                    if(detected == True and tempDetected == False):
                        detected = False
                        outBin = max(binMap, key=binMap.get)
                        print(outBin)

                        outVal = max(characterMap, key=characterMap.get)
                        if(not (outVal in fileResults)):
                            fileResults[outVal] = 0
                        fileResults[outVal] = fileResults[outVal] + 1

                        while moveActuators(outBin):
                            dummy = 1
                        for key, value in characterMap.items():
                            characterMap[key] = 0
                        characterMap["?"] = 1
                        for key, value in binMap.items():
                            binMap[key] = 0
                        binMap[1] = 1
                        #mapTimer = time.time() + 1


                    cv2.putText(image_bgr, characterOut, (5,50), 0, 1, (255,255,255), 2)
                    cv2.imshow("frame", image_bgr)
                    #cv2.imshow("frame2", mask)
                    #cv2.imshow("frame3", roi)

                    if cv2.waitKey(1) == ord('q'):
                        jsonObject = json.dumps(fileResults, indent=4)
                        outputFile.write(jsonObject)
                        break

                    if(rotorTimer < time.time()):
                        rotorTimer = time.time() + 1
                        if (rotorDirection == 1):
                            GPIO.output(rotIn1, GPIO.LOW)
                            GPIO.output(rotIn2, GPIO.HIGH)
                            rotorDirection = 2
                        else:
                            GPIO.output(rotIn1, GPIO.HIGH)
                            GPIO.output(rotIn2, GPIO.LOW)
                            rotorDirection = 1
                
        except Exception as e:
            
            print(e)
            print("There has been an error with the program. Exiting...")

        finally:
            # closing all open windows
            cv2.destroyAllWindows()
            GPIO.cleanup()


    cv2.destroyAllWindows()

GPIO.cleanup()
