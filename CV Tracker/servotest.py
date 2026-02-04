#WARNING - WILL BREAK IF ASSEMBLED

import pigpio
import time

pi = pigpio.pi()

S1 = 12
S2 = 18
S3 = 13

pi.set_mode(S1,pigpio.OUTPUT)
pi.set_mode(S2,pigpio.OUTPUT)
pi.set_mode(S3,pigpio.OUTPUT)


def set_angle(pin,angle):
	pulse = 500 + (angle/180.0) * 2000
	pi.set_servo_pulsewidth(pin,pulse)

while True:
	set_angle(S1,0)
	set_angle(S2,0)
	set_angle(S3,0)

	time.sleep(1)

	set_angle(S1,180)
	set_angle(S2,180)
	set_angle(S3,180)

	time.sleep(1)
	break
set_angle(S1,90)
set_angle(S2,90)
set_angle(S3,90)

pi.stop()
