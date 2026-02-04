from picamera2 import Picamera2
import cv2
import time

RESOLUTION = (640, 480)

LOWER = (35,  100,  30)   
UPPER = (85, 255, 255)
MINAREA = 400

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

picam2 = Picamera2()
config = picam2.create_preview_configuration(
	main={"size": RESOLUTION, "format": "RGB888"}
)
picam2.configure(config)
picam2.start()


while True:
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
			x0 = cx - side // 2
			y0 = cy - side // 2

			# Clamp square to frame bounds
			H, W = bgr.shape[:2]
			x0 = clamp(x0, 0, W - side)
			y0 = clamp(y0, 0, H - side)

			# Draw square + center
			cv2.rectangle(rgb, (x0, y0), (x0 + side, y0 + side), (255, 255, 255), 2)
			cv2.circle(rgb, (cx, cy), 4, (0, 0, 255), -1)
			print(cx,cy)
	
	#show masked view
	cv2.imshow("Picamera2 (Green Ball Tracking)", mask)
	
	#show real view
	#cv2.imshow("Picamera2 (Green Ball Tracking)", rgb)
	
	#press 'q' to end
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
                    


cv2.destroyAllWindows()
picam2.stop()
