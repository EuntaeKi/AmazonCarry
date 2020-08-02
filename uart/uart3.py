# Connecting UART between Raspberry Pi and STM32

# RPI: GPIO14 (8) - TX, GPIO15 (10) - RX
# STM: PA3 - RX, PA2 - TX

import serial
import time

def init():
	ser = serial.Serial(
		port='/dev/ttyS0',
		baudrate = 4800,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1000
	)
	return ser

def receive(ser):
	msg = ser.read(4)
	print(msg)
	dist = msg.decode('utf-8')
	#dist = int.from_bytes(msg, byteorder='big', signed=False)
	print(dist)
	try:
		dist = int(dist)
	except ValueError:
		try:
			dist = int(dist[0:-1])
		except ValueError:
			try: 
				dist = int(dist[0:-2])
			except ValueError:
				try:
					dist = int(dist[0:-3])
				except ValueError:
					try:
						dist = 8000
					except:
						pass
	dist = float(dist) * 0.00328084
	#print(dist)
	return dist

def main():
	ser = init()
	while True:	
		receive(ser)

if __name__ == "__main__":
	main()
