import tesserocr
from tesserocr import PyTessBaseAPI, PSM, OEM
import numpy
from picamera2 import Picamera2, Preview
import cv2
import time

from PIL import Image
from PIL import ImageOps

validText = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

print(tesserocr.tesseract_version())  # print tesseract-ocr version
#print(tesserocr.get_languages())  # prints tessdata path and list of available languages

image = cv2.imread('Z.jpg')

#imgBlur = cv2.blur(image, (7,7))

imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

imgBlur = cv2.blur(imgGray, (7,7))

ret, imgBinary = cv2.threshold(imgBlur, 70, 255, cv2.THRESH_BINARY) 
#cv2.imshow("test", imgBinary)
#cv2.waitKey(1000)

#imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

imPil = Image.fromarray(imgBinary)

#imPilGray = ImageOps.grayscale(imPil)

imPil.show()

with PyTessBaseAPI(psm=10) as api:
    #api.setPageSegMode()
    api.SetVariable('tessedit_char_whitelist', validText)
    api.SetImage(imPil)
    conf = api.MeanTextConf()
    print("Text:", api.GetUTF8Text())
    print("Confidence:", conf)


# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.