# Written By:	 Euntae Ki, Seungjae Moon, Alan Reyes, Dylan Lam
# Functionality: Main python script that manages and calls other python scripts.
#		 All the data from peripheral will pass through this script to be transmitted to the web server.
#		 Manages motor movement, camera instantiation, and  
#

# Import relevant libraries
import importlib.util
import os
import time
import pickle
import sys
import select
import json

# Call other python scripts
spec1 = importlib.util.spec_from_file_location("uart.py", "./uart/uart.py")
spec2 = importlib.util.spec_from_file_location("RobotControlMecanum.py", "./motor/RobotControlMecanum.py")

uart = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(uart)

motor = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(motor)

# Initial variable declaration
time.sleep(5)
x = -9999
is_object_detected = False
ser = uart.init()
dist = 0
setDist = 3
detectPress = False
remote = False
remoteControl=''
motorMove = ''

# While loop to keep the system going indefinitely
while True:
	# If the pickle file for detection exists, then read in the values for the object detection status
	if (os.path.exists('is_detection.pkl')):
		with open('is_detection.pkl', 'rb') as pickle_file:
			try:			
				is_object_detected = pickle.load(pickle_file)
			except EOFError:
				pass

	# If the object is detected, read in the x-coordinate of the object
	if (is_object_detected == True):
		# Get x-coordinate from pi Camera
		if (os.path.exists('xavg.pkl')):
			with open('xavg.pkl', 'rb') as pickle_file:
				try:			
					x = pickle.load(pickle_file)
				except EOFError:
					pass

		# Get distance from VCSEL sensor once the object is detected
		dist = uart.receive(ser)

	# Slight delay for web server communication
	time.sleep(0.05)
	
	# Check if there is something to read in from the webserver.js file
	# Without this checking process, the whole system will get blocked by stdin.readline() command
	if select.select([sys.stdin,],[],[],0.0)[0]:
		lines = sys.stdin.readline()
		if not lines:
			print("Error: Emptry String")
		else:	# Parse the JSON it recieved from the web server 
			parsed = json.loads(lines)
			if parsed["type"] == "control":
				remoteControl = parsed["data"]
			elif parsed["type"] == "manual":
				remote = parsed["data"]
				with open("remote.pkl", 'wb') as pickle_file:
					pickle.dump(remote, pickle_file)
			elif parsed["type"] == "customDistance":
				setDist = parsed["data"]
			elif parsed["type"] == "detectCue":
				detectPress = parsed["data"]
				with open("detectPress.pkl", 'wb') as pickle_file:
					pickle.dump(detectPress, pickle_file)
					os.system("sudo chmod 777 detectPress.pkl")

	# Dump updated data to the web server in JSON format and flush it
	inputToNode = json.dumps({"distance": dist, "camera": is_object_detected, "Remote":remote, "detectCue": detectPress})
	print(inputToNode)
	sys.stdout.flush()

	# Move motor based on x-coordinate, distance, and remote status
	if remote:
		motor.move2(remoteControl)
		remoteControl = ''	# Reset the remoteControl to stop the motor
	else:	
		motor.move(x, dist, setDist, is_object_detected)
