#This is the first edition of a full code controlling each of the electrical componmotor1ents
#Electrical components include:
#   6 linear actuators
#   2 DC Motors
#Linear Actuator control:
#   Linear actuators are controlled using two input signals
#   The linear actuator moves by introducing a voltage difference to its two ends
#   Therefore, by having two input wires, we can control a linear actuator in both directions
#   By having input 1 high and input 2 low, we can move the actuator left
#   By applying the reverse polarity, we can move it right
#   Total wires used by linear actuators is 2 wires per actuator * 6 actuators = 12 wires
#DC Motor control
#   We have two DC motors
#   With our current system design, they need to move only in one direction.
#   We control the motor speed by a PWM signal
#   For our purposes, a software-based PWM is a perfectly fine solution
#   Once again, this DC motor is controlled by applying a voltage difference to its inputs
#   We need an additional input to our Motor Controller for the PWM signal
#   Therefore, we need 3 wires pero DC Motor * 2 DC Motors = 6 wires
#   If needed, these can be reduced to 2 wires per DC motor,
#   because we only need one direction, so one of the inputs can be ground as it will never go high
#ACTUATOR STATUS CONTROL
#As actuators have no feedback, we need to manually keep track of each actuator's current position
#This will be done by using an internal variable, 0 for left, 1 for middle, 2 for right
#Furthermore, for timing, we will be using variables keeping track of when movement started and ended

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
    #The higher the bin level, the more actuators we need to move
    #Want to make more common values be bins 1,2,3,4 etc
    if(binNumber == 1):
        #Move act1 to right only if its not doing any current movement and not in position already
        if(act1pos != 2):
            if(not act1on):
                moveAct1Right()
                act1on = True
                if(act1pos == 0):
                    act1timer = time.time() + act1delay * 2
                else:
                    act1timer = time.time() + act1delay
                act1pos = 2
    
    elif(binNumber == 2):
        #Move act1 to left only if its not doing any current movement and not in position already
        if(act1pos != 0):
            if(not act1on):
                moveAct1Left()
                act1on = True
                if(act1pos == 2):
                    act1timer = time.time() + act1delay * 2
                else:
                    act1timer = time.time() + act1delay
                act1pos = 0
    
    elif(binNumber == 3):
        #Move act1 to middle
        if(act1pos == 0):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = 1
        elif(act1pos == 2):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = 1
        #Move act2 to right only if its not doing any current movement and not in position already
        if(act2pos != 2):
            if(not act2on):
                moveAct2Right()
                act2on = True
                if(act2pos == 0):
                    act2timer = time.time() + act2delay * 2
                else:
                    act2timer = time.time() + act2delay
                act2pos = 2   
    
    elif(binNumber == 4):
        #Move act1 to middle
        if(act1pos == 0):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = 1
        elif(act1pos == 2):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = 1
        #Move act2 to left only if its not doing any current movement and not in position already
        if(act2pos != 0):
            if(not act2on):
                moveAct2Left()
                act2on = True
                if(act2pos == 2):
                    act2timer = time.time() + act2delay * 2
                else:
                    act2timer = time.time() + act2delay
                act2pos = 0

    elif(binNumber == 5):
        #Move act1 to middle
        if(act1pos == 0):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = 1
        elif(act1pos == 2):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = 1
        #Move act2 to middle
        if(act2pos == 0):
            if(not act2on):
                moveAct2Right()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = 1
        elif(act2pos == 2):
            if(not act2on):
                moveAct2Left()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = 1
        #Move act 3 to right
        if(act3pos != 2):
            if(not act3on):
                moveAct3Right()
                act3on = True
                if(act3pos == 0):
                    act3timer = time.time() + act3delay * 2
                else:
                    act3timer = time.time() + act3delay
                act3pos = 2  

    elif(binNumber == 6):
        #Move act1 to middle
        if(act1pos == 0):
            if(not act1on):
                moveAct1Right()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = 1
        elif(act1pos == 2):
            if(not act1on):
                moveAct1Left()
                act1on = True
                act1timer = time.time() + act1delay
                act1pos = 1
        #Move act2 to middle
        if(act2pos == 0):
            if(not act2on):
                moveAct2Right()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = 1
        elif(act2pos == 2):
            if(not act2on):
                moveAct2Left()
                act2on = True
                act2timer = time.time() + act2delay
                act2pos = 1
        #Move act 3 to left
        if(act3pos != 0):
            if(not act3on):
                moveAct3Left()
                act3on = True
                if(act3pos == 2):
                    act3timer = time.time() + act3delay * 2
                else:
                    act3timer = time.time() + act3delay
                act3pos = 0
    
    #Turn off beads that have reachd their time limit
    if(act1timer < time.time()):
        turnOffAct1()
    if(act2timer < time.time()):
        turnOffAct2()
    if(act3timer < time.time()):
        turnOffAct3()
    if(act4timer < time.time()):
        turnOffAct4()
    if(act5timer < time.time()):
        turnOffAct5()
    if(act6timer < time.time()):
        turnOffAct6()
    




            

    


    



#Import libraries
import RPi.GPIO as GPIO          
from time import sleep
import time

#GPIO and Variable Assignmments
#in and en variables represent pins, while pos and timer are software variables
#ACTUATOR 1
act1in1 = 2
act1in2 = 3
act1pos = 0
act1timer = 0
act1on = False
act1delay = 0.09
#ACTUATOR 2
act2in1 = 19
act2in2 = 26
act2pos = 0
act2timer = 0
act2on = False
act2delay = 0.09
#ACTUATOR 3
act3in1 = 19
act3in2 = 26
act3pos = 0
act3timer = 0
act3on = False
act3delay = 0.09
#ACTUATOR 4
act4in1 = 14
act4in2 = 18
act4pos = 0
act4timer = 0
act4on = False
act4delay = 0.09
#ACTUATOR 5
act5in1 = 23
act5in2 = 24
act5pos = 0
act5timer = 0
act5on = False
act5delay = 0.09
#ACTUATOR 6
act6in1 = 20
act6in2 = 21
act6pos = 0
act6timer = 0
act6on = False
act6delay = 0.09

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
#MOTOR 1 INITIALIZATION
# GPIO.setup(motor1in, GPIO.OUT)
# GPIO.output(motor1in, GPIO.LOW)
# GPIO.setup(motor1en, GPIO.OUT)
#p=GPIO.PWM(motor1en, 10000)
#p.start(0)

#ACTUATOR CALIBRATION
print("GPIO set!")
print("Calibrating actuators by moving them to the left...(TEMPORARY)")
#TEMPORARY CODE
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
while((tempTime + 0.10) > time.time()):
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

print("\n")
print("Actuators set! Type the number bin position to make it change values")
print("Type e to exit")
print("\n")    

while(1):
    x=input().strip()
    
    if x=='1':
        print("Moving Actuator 1")
        if(act1pos==2):
            GPIO.output(act1in1,GPIO.HIGH)
            GPIO.output(act1in2,GPIO.LOW)
            print("Moving Left")
            act1pos = 0
            x='z'
        else:
            GPIO.output(act1in1,GPIO.LOW)
            GPIO.output(act1in2,GPIO.HIGH)
            print("Moving Right")
            act1pos = 2
            x='z'


    elif x=='2':
        print("Moving Actuator 2")
        if(act2pos==2):
            GPIO.output(act2in1,GPIO.HIGH)
            GPIO.output(act2in2,GPIO.LOW)
            print("Moving Left")
            act2pos = 0
            x='z'
        else:
            GPIO.output(act2in1,GPIO.LOW)
            GPIO.output(act2in2,GPIO.HIGH)
            print("Moving Right")
            act2pos = 2
            x='z'

    elif x=='3':
        print("Moving Actuator 3")
        if(act3pos==2):
            GPIO.output(act3in1,GPIO.HIGH)
            GPIO.output(act3in2,GPIO.LOW)
            print("Moving Left")
            act3pos = 0
            x='z'
        else:
            GPIO.output(act3in1,GPIO.LOW)
            GPIO.output(act3in2,GPIO.HIGH)
            print("Moving Right")
            act3pos = 2
            x='z'

    elif x=='4':
        print("Moving Actuator 4")
        if(act4pos==2):
            GPIO.output(act4in1,GPIO.HIGH)
            GPIO.output(act4in2,GPIO.LOW)
            print("Moving Left")
            act4pos = 0
            x='z'
        else:
            GPIO.output(act4in1,GPIO.LOW)
            GPIO.output(act4in2,GPIO.HIGH)
            print("Moving Right")
            act4pos = 2
            x='z'

    elif x=='5':
        print("Moving Actuator 5")
        if(act5pos==2):
            GPIO.output(act5in1,GPIO.HIGH)
            GPIO.output(act5in2,GPIO.LOW)
            print("Moving Left")
            act5pos = 0
            x='z'
        else:
            GPIO.output(act5in1,GPIO.LOW)
            GPIO.output(act5in2,GPIO.HIGH)
            print("Moving Right")
            act5pos = 2
            x='z'

    elif x=='6':
        print("Moving Actuator 6")
        if(act6pos==2):
            GPIO.output(act6in1,GPIO.HIGH)
            GPIO.output(act6in2,GPIO.LOW)
            print("Moving Left")
            time.sleep(0.168)
            act6pos = 0
            GPIO.output(act6in1,GPIO.LOW)
            GPIO.output(act6in2,GPIO.LOW)
            x='z'
        else:
            GPIO.output(act6in1,GPIO.LOW)
            GPIO.output(act6in2,GPIO.HIGH)
            print("Moving Right")
            time.sleep(0.168)
            GPIO.output(act6in1,GPIO.LOW)
            GPIO.output(act6in2,GPIO.LOW)
            act6pos = 2
            x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        print("Cleand GPIO")
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
#GPIO.cleanup()