import RPi.GPIO as GPIO          
from time import sleep
import time

GPIO.cleanup()


in1 = 21
in2 = 20
en = 26
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,15)
p.start(25)
print("\n")
#print("The default speed & direction of motor is LOW & Forward.....")
print("r-run e-exit")
print("\n")    

tempTime = time.time() + 4

while(time.time() < tempTime):

    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    #print("forward")
    # time.sleep(0.02)
    # GPIO.output(in1,GPIO.LOW)
    # GPIO.output(in2,GPIO.LOW)
    # time.sleep(0.07)
    
        

GPIO.cleanup()