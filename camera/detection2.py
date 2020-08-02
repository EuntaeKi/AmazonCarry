import numpy as np
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import dlib
import time
import pickle

#def xcoordinate(val):
#	return val
VAL = 0

# Possible objects this DNN can detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

X_RESOLUTION = 640
Y_RESOLUTION = 480
BUFFER = X_RESOLUTION * 0.15
CONFIDENCE_CHECK = 6
# Camera setup
camera = PiCamera()
camera.resolution = (X_RESOLUTION,Y_RESOLUTION)
camera.framerate = 30
video_feed = PiRGBArray(camera, size=(X_RESOLUTION,Y_RESOLUTION))

# For image scaling
scale_factor = 1

# Probability threshold to ensure detections are accurate
prob_threshold = 0.8

# Set up network
net = cv2.dnn.readNetFromCaffe("/home/pi/Scripts/camera/deploy.prototxt", "/home/pi/Scripts/camera/mobilenet_iter_73000.caffemodel")

# Set up tracker
#tracker = dlib.correlation_tracker()
test_tracker = cv2.TrackerKCF_create()
is_obj_detected = False

# Frame rate set up
fr_calc = 1
freq = cv2.getTickFrequency()

# Font
font = cv2.FONT_HERSHEY_SIMPLEX

# Variables used to check if user is off-centered
is_object_off_centered = False
off_center_t1 = time.time()
off_center_t2 = off_center_t1

# Camera warm-up
time.sleep(0.1)

for frame in camera.capture_continuous(video_feed, format="bgr", use_video_port=True):
	t1 = cv2.getTickCount()

	image = frame.array

	(h,w,d) = image.shape

	"""if is_obj_detected == False:
		# Image Processing
		blob = cv2.dnn.blobFromImage(cv2.resize(image, (300,300)), 0.007843, (300, 300), 127.5)

		# Insert processed image into DNN and get detections
		net.setInput(blob)
		detections = net.forward()

		# Go through every detection check if it's probability is greater than 0.8 and create a box on the original image
		for i in range(detections.shape[2]):
			probability = detections[0,0,i,2]
			# Gets index of CLASS of detected object
			class_index = int(detections[0,0,i,1])
			# 3:7 corresponds to box coordinates
			box = detections[0,0, i, 3:7] * np.array([w,h,w,h])
			(x0, y0, x1, y1) = box.astype("int")
			x_avg = int((x0 + x1)/2)

			if probability > prob_threshold and class_index == 15 and x_avg > int(X_RESOLUTION/2 - BUFFER) and x_avg < int(X_RESOLUTION/2 + BUFFER):
				is_obj_detected = True

				# Label for prediction
				label = "{}: {:.2f}%".format(CLASSES[class_index], probability * 100)

				# Initialize Tracker
				#tracker_rectangle = dlib.rectangle(x0,y0,x1,y1)
				#tracker.start_track(image, tracker_rectangle)
				bbox = (x0, y0, x1-x0, y1-y0)
				ok = test_tracker.init(image, bbox)

				# Creates box
				cv2.rectangle(image, (x0,y0), (x1,y1), (0,0,255), 2)
				# Creates text for box
				cv2.putText(image, label, (x0,y0), font, 0.5*scale_factor, (0,0,255), 2)
				# Only track first object found
				break
		


	else:
		# Update tracker, get confidence level,  and get new coordinates
		(success, box) = test_tracker.update(image)
		#print(confidence)
		#new_rect_coord = tracker.get_position()
		#x0 = int(new_rect_coord.left())
		#y0 = int(new_rect_coord.top())
		#x1 = int(new_rect_coord.right())
		#x2 = int(new_rect_coord.bottom())
		# If confidence integer is not high enough, then break from for loop
		#if confidence < CONFIDENCE_CHECK:
		#	break
		x_avg = int((x0+x1)/2)
		#xcoordinate(x_avg)
		VAL = x_avg
		with open("xavg.pkl", 'wb') as pickle_file:
			pickle.dump(x_avg, pickle_file)

		if x_avg < BUFFER or x_avg > X_RESOLUTION - BUFFER:
			if is_object_off_centered == False:
				off_center_t1 = time.time()
				is_object_off_centered = True
			else:
				off_center_t2 = time.time()
		else:
			is_object_off_centered = False

		if off_center_t2 - off_center_t1 > 5:
			is_obj_detected = False
			off_center_t1 = 0
			off_center_t2 = 0
		
		if success:
			print('hi')
			(x0,y0,width,height) = [int(u) for u in box]
			label = "{}%".format(CLASSES[class_index])
			cv2.rectangle(image,(x0,y0), (x0 + width,y0 + height), (0,0,255), 2)
			cv2.putText(image, label, (x0,y0), font, 0.5*scale_factor, (0,0,255), 2)

	"""
	with open("is_detection.pkl", 'wb') as pickle_file:
		pickle.dump(is_obj_detected, pickle_file)

	cv2.putText(image, "FPS: {0: .2f}".format(fr_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

	cv2.imshow("Output", image)

	t2 = cv2.getTickCount()
	del_t = (t2-t1)/freq
	fr_calc = 1/del_t

	video_feed.truncate(0)
	key =  cv2.waitKey(1)
	if key == ord('q'):
		break



