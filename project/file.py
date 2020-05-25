import io
import time
import cv2
import numpy as np
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import datetime
import os

colors = {"blue":(255,200,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
faceCascade = cv2.CascadeClassifier('/home/pi/Documents/project/faces.xml')
noseCascade = cv2.CascadeClassifier('/home/pi/Documents/project/nose.xml')
mouthCascade = cv2.CascadeClassifier('/home/pi/Documents/project/mouth.xml')
masks = 0
nomasks = 0

# saves to logs
def save(time):
	global masks
	global nomasks
	date = datetime.date.today().strftime("%Y-%m-%d")
	script_dir = os.path.dirname(__file__)
	rel_path = "logs/" + date + ".txt"
	file_dir = os.path.join(script_dir, rel_path)
	file_log = open(file_dir, 'at')
	file_log.write(time+"-> Mask: " + str(masks) + " No mask: " + str(nomasks) + "\n")
	file_log.close()
	
# draws bounding box around faces and checks for other features
def draw_boundary(img):
	color = colors['green']
	text = "Mask"
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	features = faceCascade.detectMultiScale(gray_img, 1.1, 10) 
	for(x,y,w,h) in features:
		coords = [x,y,w,h]
		roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
		gray_img = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
		noseFeatures = noseCascade.detectMultiScale(gray_img, 1.4, 4)
		mouthFeatures = mouthCascade.detectMultiScale(gray_img, 1.4, 20)
		# mask detection based off whether nose features and mouth features are detected
		if(len(noseFeatures)>0 or len(mouthFeatures)>0):
			roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
			color = colors['red']
			text = "No Mask"
			'''		
			for(a,b,c,d) in noseFeatures:
				cv2.rectangle(img, (x+a,y+b), (x+a+c, y+b+d), colors['blue'], 2)  # blue - nose
			for(a,b,c,d) in mouthFeatures:
				cv2.rectangle(img, (x+a,y+b), (x+a+c, y+b+d), colors['white'], 2)  # white - mouth
			'''
		
		cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
		cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1)
		if(text == "Mask"):
			global masks
			masks += 1
		elif(text == "No Mask"):
			global nomasks
			nomasks += 1
	return img

# camera setup
vs = VideoStream(src=0).start()			 
time.sleep(2.0)
fps = FPS().start()

# for each captured frame
while True:
	masks = 0
	nomasks = 0
	frame = vs.read()
	frame = imutils.resize(frame,width=320,height=240)
	frame = draw_boundary(frame)
	time = datetime.datetime.now()
	time_text = time.strftime("%H:%M:%S")
	cv2.putText(frame, time_text, (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, colors['white'], 2)
	cv2.putText(frame, "Wearing mask: " + str(masks), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, colors['green'], 2)
	cv2.putText(frame, "Not wearing: " + str(nomasks), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, colors['red'], 2)
	cv2.imshow("Face detection", frame)
	if(masks>0 or nomasks>0):
		save(time_text)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
	fps.update()
	
fps.stop()
cv2.destroyAllWindows()
vs.stop()
