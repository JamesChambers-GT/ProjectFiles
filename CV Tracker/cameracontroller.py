#return coordinates of the ball each frame

from picamera2 import Picamera2
import cv2
import time
import math


LOWER = (35,  100,  30)   
UPPER = (85, 255, 255)
MINAREA = 400

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

               

def coords(picam2):
	rgb = picam2.capture_array()
	bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
	blurred = cv2.GaussianBlur(bgr, (5, 5), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, LOWER, UPPER)

	contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	if contours:	
		bestguess = max(contours, key=cv2.contourArea)
		area = cv2.contourArea(bestguess)
		if area > MINAREA:
			ball = bestguess
			x, y, w, h = cv2.boundingRect(ball)
			side = max(w, h)
			cx = x + w // 2
			cy = y + h // 2

			return(cx,cy)
		else:
			return(-5000,-5000)
	else:
		return(-5000,-5000)
