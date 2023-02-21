import tesserocr
from tesserocr import PyTessBaseAPI, PSM, OEM
import numpy
from picamera2 import Picamera2, Preview
import cv2
import time

from PIL import Image

validText = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

print(tesserocr.tesseract_version())  # print tesseract-ocr version
#print(tesserocr.get_languages())  # prints tessdata path and list of available languages

image = cv2.imread('../../testImages/OCR/Q.jpg')

imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

imPil = Image.fromarray(imageRGB)

with PyTessBaseAPI(psm=6) as api:
    #api.setPageSegMode()
    api.SetVariable('tessedit_char_whitelist', validText)
    api.SetImage(imPil)
    print(api.GetUTF8Text())


# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.