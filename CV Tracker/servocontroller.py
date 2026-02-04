#allow for control of both servo axes
low1 = 12
low2 = 13
upper = 18


def angle2pulse(angle):
	return 500 + (angle/180.0) * 2000
	

def set_angle(pin,angle, pi):
	pulse = angle2pulse(angle)
	pi.set_servo_pulsewidth(pin,pulse)
	
	
def set_pitch(pi, angle):
	set_angle(low1,angle, pi)
	opposite = 180-angle
	set_angle(low2,opposite, pi)
	print(f"pitch to {angle}")
	
def set_yaw(pi, angle):
	set_angle(upper,angle, pi)
	print(f"yaw to {angle}")

def neutral(pi):
	set_pitch(pi, 90)
	set_yaw(pi, 90)
	print("Axes neutral")
	

def test_high():
	neutral()
	time.sleep(1)
	set_yaw(0)
	time.sleep(1)
	set_yaw(180)
	time.sleep(1)
	neutral()


