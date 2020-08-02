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
	msg = ser.read(2)
	#print(msg)
	dist = int.from_bytes(msg, byteorder='little', signed=False)
	dist = float(dist) * 0.00328084
	#print(dist)
	return dist

def main():
	ser = init()
	while True:	
		receive(ser)

if __name__ == "__main__":
	main()

