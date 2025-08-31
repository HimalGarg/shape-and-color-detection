from shapedetector import *
from centre_of_shape import *
from color_detector import *
import argparse
import imutils
import cv2 

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True, help="path to the input image")

args=vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sno=1
# loop over the contours
for c in cnts:
	
	cX, cY = findCentroid(c)
	shape = detect(c)
	color = get_color(image, c)
	color_shape = f"{color} {shape}"
	print(f"{sno}. {color_shape} at ({cX},{cY})")
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, color_shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
	cv2.imshow("Image", image)
	sno+=1
	cv2.waitKey(0)