#!/usr/bin/env python
# Adapted from Ingmar Stapel

import sys, tty, termios, os, readchar
import L298NHBridgeMecanum as HBridge

# Define global speeds of left and right motors
speedleft = 0
speedright = 0

# Prints the program menu for the user
print("w/s: forward or backward")
print("a/d: rotate left or right")
print("y/c: move left or right")
print("q: stop the motors")
print("x: exit")

# Reads keyboard input from the user
def getch():
   ch = readchar.readchar()
   return ch

# Prints the program menu and displays the current speed of the motors
def printscreen():
   # Clears the screen contents
   os.system('clear')
   print("w/s: forward or backward")
   print("a/d: rotate left or right")
   print("y/c: go left or right")
   print("q: stop the motors")
   print("x: exit")
   print("Speed of left motors: ", speedleft)
   print("Speed of right motors: ", speedright)

while True:
   char = getch()
   
   # Accelerate forward
   if(char == "w"):
      # Increase duty cycle of all PWM pins by 10%
      speedleft = speedleft + 0.1
      speedright = speedright + 0.1

      if speedleft > 1:
         speedleft = 1
      if speedright > 1:
         speedright = 1
      
      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      printscreen()

   # Accelerate backward
   if(char == "s"):
      # Decrease duty cycle of all PWM pins by 10%
      speedleft = speedleft - 0.1
      speedright = speedright - 0.1

      if speedleft < -1:
         speedleft = -1
      if speedright < -1:
         speedright = -1
              
      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      printscreen()

    # Stop all motors
   if(char == "q"):
      speedleft = 0
      speedright = 0
      HBridge.setMotorDirection("leftmotor_back", speedleft)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright)
      HBridge.setMotorDirection("rightmotor_front", speedright)  
      printscreen()

   # Rotate right
   if(char == "d"):      
      speedright = speedright - 0.1
      speedleft = speedleft + 0.1
      
      if speedright < -1:
         speedright = -1
      
      if speedleft > 1:
         speedleft = 1

      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      printscreen()

   # Move sideways to the left
   if(char == "c"):      
      speedright = speedright - 0.1
      speedleft = speedleft + 0.1
      
      if speedright < -1:
         speedright = -1
      
      if speedleft > 1:
         speedleft = 1

      HBridge.setMotorDirection("leftmotor_back", speedleft)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      printscreen()
      
   # Rotate left
   if(char == "a"):
      speedleft = speedleft - 0.1
      speedright = speedright + 0.1
         
      if speedleft < -1:
         speedleft = -1
      
      if speedright > 1:
         speedright = 1

      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      printscreen()

   # Move sideways to the right
   if(char == "y"):
      speedleft = speedleft - 0.1
      speedright = speedright + 0.1
         
      if speedleft < -1:
         speedleft = -1
      
      if speedright > 1:
         speedright = 1

      HBridge.setMotorDirection("leftmotor_back", speedleft)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      printscreen()
      
   # Exit program
   if(char == "x"):
      HBridge.setMotorDirection("leftmotor_back", 0)
      HBridge.setMotorDirection("leftmotor_front", 0)
      HBridge.setMotorDirection("rightmotor_back", 0)
      HBridge.setMotorDirection("rightmotor_front", 0)  
      HBridge.exit()
      print("Program successfully ended")
      break
   
   # Dumb variable char
   char = ""
   
