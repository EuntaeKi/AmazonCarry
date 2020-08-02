import os
import time
import pickle

os.system("python /home/pi/Scripts/camera/detection.py &")
time.sleep(5)
x = -9999
while True:
	if (os.path.exists('xavg.pkl')):
		with open('xavg.pkl', 'rb') as pickle_file:
			try:			
				x = pickle.load(pickle_file)
			except EOFError:
				pass
	print(x)
