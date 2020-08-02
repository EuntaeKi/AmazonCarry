# Written By:	 Alan Reyes
# Functionality: Object detection and tracking script. Initially, this script takes images from
#		 the PiCamera and puts them through a Deep Neural Network to identify (location)
#		 and classify (name) all objects in an image. Once a person is detected in the middle of
#		 the frame, this script starts tracking the user with the dlib tracker. All data that
#		 setup.py needs or that this script from setup.py is sent and received through pkl files.
#		 FPS is also calculated to determine efficiency of detection/tracking.

# Import relevant libraries
import numpy as np
import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
import dlib
import time
import pickle

# Possible objects this DNN can detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# Resolution and buffer constants
X_RESOLUTION = 640
Y_RESOLUTION = 480
BUFFER = X_RESOLUTION * 0.15

# Camera setup
camera = PiCamera()
camera.resolution = (X_RESOLUTION,Y_RESOLUTION)
camera.framerate = 30
video_feed = PiRGBArray(camera, size=(X_RESOLUTION,Y_RESOLUTION))
video_feed.truncate(0)
video_feed.seek(0)


# Probability threshold to ensure detections are accurate
prob_threshold = 0.8

# Set up network
net = cv2.dnn.readNetFromCaffe("/home/pi/Scripts/camera/deploy.prototxt", "/home/pi/Scripts/camera/mobilenet_iter_73000.caffemodel")

# Set up tracker
tracker = dlib.correlation_tracker()

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

# User interface signals
detectPress = False
remote = False

for frame in camera.capture_continuous(video_feed, format="bgr", use_video_port=True):
	t1 = cv2.getTickCount()
	if (os.path.exists('detectPress.pkl')):
		with open('detectPress.pkl', 'rb') as pickle_file:
			try:
				detectPress = pickle.load(pickle_file)
			except EOFError:
				pass
	
	if (os.path.exists('remote.pkl')):
		with open('remote.pkl', 'rb') as pickle_file:
			try:
				remote = pickle.load(pickle_file)
			except EOFError:
				pass


	image = frame.array

	(h,w,d) = image.shape
	if is_obj_detected == False and detectPress:
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
				tracker_rectangle = dlib.rectangle(x0,y0,x1,y1)
				tracker.start_track(image, tracker_rectangle)

				detectPress = False

				with open("detectPress.pkl", 'wb') as pickle_file:
					pickle.dump(detectPress, pickle_file)

				# Creates box
				cv2.rectangle(image, (x0,y0), (x1,y1), (0,0,255), 2)
				# Creates text for box
				cv2.putText(image, label, (x0,y0), font, 0.5, (0,0,255), 2)
				# Only track first object found
				break
		


	elif is_obj_detected:
		# Update tracker, get confidence level, and get new coordinates
		confidence = tracker.update(image)
		new_rect_coord = tracker.get_position()
		x0 = int(new_rect_coord.left())
		y0 = int(new_rect_coord.top())
		x1 = int(new_rect_coord.right())
		x2 = int(new_rect_coord.bottom())

		# Average x coordinates and save as pkl file for setup.py to receive variable info
		x_avg = int((x0+x1)/2)
		with open("xavg.pkl", 'wb') as pickle_file:
			pickle.dump(x_avg, pickle_file)

		# Set timer if object is too far to the right or left
		if x_avg < BUFFER or x_avg > X_RESOLUTION - BUFFER:
			if is_object_off_centered == False:
				off_center_t1 = time.time()
				is_object_off_centered = True
			else:
				off_center_t2 = time.time()
		else:
			is_object_off_centered = False

		# If timer lasts for 5 seconds then object is no longer detected and needs to redetect
		if off_center_t2 - off_center_t1 > 5:
			is_obj_detected = False
			off_center_t1 = 0
			off_center_t2 = 0
		
		# Create label and add rectangle and label to image
		label = "{}: {:.2f}%".format(CLASSES[class_index], confidence)
		cv2.rectangle(image,(x0,y0), (x1,y1), (0,0,255), 2)
		cv2.putText(image, label, (x0,y0), font, 0.5, (0,0,255), 2)

	
	# Update pkl file with detection boolean for setup.py
	with open("is_detection.pkl", 'wb') as pickle_file:
		pickle.dump(is_obj_detected, pickle_file)

	cv2.putText(image, "FPS: {0: .2f}".format(fr_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

	cv2.imshow("Output", image)

	t2 = cv2.getTickCount()

	# Calculate FPS
	del_t = (t2-t1)/freq
	fr_calc = 1/del_t
	
	video_feed.truncate(0)
	video_feed.seek(0)
	
	key =  cv2.waitKey(1)
	if key == ord('q'):
		break

cv2.destroyAllWindows()

