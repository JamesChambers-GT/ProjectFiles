#united control
#use servocontroller.py and cameracontroller.py to track ball
#theta is yaw angle, alpha is pitch angle


from servocontroller import set_pitch, set_yaw, neutral
from cameracontroller import coords

import time
import math

import pigpio

from picamera2 import Picamera2
import cv2


#servo setup
pi = pigpio.pi()
assert pi.connected, "pigpio not connected"
pi.set_mode(12,pigpio.OUTPUT)
pi.set_mode(13,pigpio.OUTPUT)
pi.set_mode(18,pigpio.OUTPUT)
theta = 90
alpha = 90
neutral(pi)

#camera setup
resx = 640
resy = 480
RESOLUTION = (resx,resy)
CoF = (resx/2,resy/2)
picam2 = Picamera2()
config = picam2.create_preview_configuration(
	main={"size": RESOLUTION, "format": "RGB888"}
)
picam2.configure(config)
picam2.start()

time.sleep(1)
#===================================================
#Main Process

p_gain_theta = 1.0/32
p_gain_alpha = 1.0/24
freq = 50 #hertz

#returns vector pointing towards ball from center of frame
def error():
	pos = coords(picam2)
	dx = -pos[0]+CoF[0]
	dy = -pos[1]+CoF[1]
	return (dx,dy)

def newTheta():
	dTheta = 0
	e = error()[0]
	if abs(e) > 500: 
		return dTheta
	if abs(e) < 32: 
		return dTheta
	else: 
		dTheta = -p_gain_theta * e
	return dTheta
		
def newAlpha():
	dAlpha = 0
	e = error()[1]
	print(f"e: {e}")
	if abs(e) > 500: 
		return dAlpha
	if abs(e) < 32: 
		return dAlpha
	else: 
		dAlpha = -p_gain_alpha * e
	return dAlpha
	

def clamp(v, lo, hi):
    return max(lo, min(hi, v))


print("Starting now")
last_time = time.time()
dt = 1.0 / freq

while True:
	if time.time() > last_time + dt:
		
		dTheta = newTheta()
		theta += dTheta
		dAlpha = newAlpha()
		alpha += dAlpha
		

		
		theta = clamp(theta, 0, 180)
		alpha = clamp(alpha, 0, 135)
		
		set_yaw(pi,theta)
		set_pitch(pi,alpha)
		
		
		last_time = time.time()
	
		

#===================================================

#servo shutdown
pi.stop()

#camera shutdown
cv2.destroyAllWindows()
picam2.stop()
