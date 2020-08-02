#!/usr/bin/env python
# Adapted from Ingmar Stapel

import sys, tty, termios, os, time
import L298NHBridgeMecanum as HBridge

center_x = 320
epsilon_x = 80
#set_dist = 2
max_dist = 6.6
epsilon_dist = 0.5

# Define global speeds of left and right motors
speedleft = 0
speedright = 0

# Prints the program menu for the user
#print("w/s: forward or backward")
#print("a/d: rotate left or right")
#print("y/c: move left or right")
#print("q: stop the motors")
#print("x: exit")

# Reads keyboard input from the user
#def getch():
   #ch = readchar.readchar()
   #return ch

# Prints the program menu and displays the current speed of the motors
def printscreen():
   global speedleft
   global speedright
   # Clears the screen contents
   os.system('clear')
   print("w/s: forward or backward")
   print("a/d: rotate left or right")
   print("y/c: go left or right")
   print("q: stop the motors")
   print("x: exit")
   print("Speed of left motors: ", speedleft)
   print("Speed of right motors: ", speedright)

#def move(curr_x, curr_dist, is_object_detected, remoteControl = 'n'):
def move(curr_x, curr_dist, raw_set_dist, is_object_detected):
   global center_x
   global epsilon_x
   #global set_dist
   global max_dist
   global epsilon_dist
   global speedleft
   global speedright
   #char = getch()
   set_dist = int(raw_set_dist)
   char = 'm'

   # Stop all motors
   if((center_x < curr_x + epsilon_x and center_x > curr_x - epsilon_x and set_dist < curr_dist + epsilon_dist and set_dist > curr_dist - epsilon_dist) or not is_object_detected):
      #print("stopped")
      speedleft = 0
      speedright = 0
      HBridge.setMotorDirection("leftmotor_back", speedleft)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      #return "Stopped"
      #printscreen()

   # Rotate right
   elif (center_x < curr_x - epsilon_x):
      #print('right')
   #if (char == "d"):      
      #speedright = speedright - 0.1
      #speedleft = speedleft + 0.1
      speedright = -0.4
      speedleft = 0.4

      if speedright < -1:
         speedright = -1
      
      if speedleft > 1:
         speedleft = 1

      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      #return "Right"

   # Rotate left
   elif (center_x > curr_x + epsilon_x):
      #print('left')
   #elif (char == "a"):
      #speedleft = speedleft - 0.1
      #speedright = speedright + 0.1
      speedright = 0.4
      speedleft = -0.4
         
      if speedleft < -1:
         speedleft = -1
      
      if speedright > 1:
         speedright = 1

      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      #return "Left"
      #printscreen()
      #printscreen()


   # Accelerate forward
   elif (set_dist < curr_dist - epsilon_dist):
   #if(char == "w"):
      #print('forward')
      # Increase duty cycle of all PWM pins by 10%
      #speedleft = speedleft + 0.01
      #speedright = speedright + 0.01
      speedleft = 0.35
      speedright = 0.35
      if speedleft > 1:
         speedleft = 1
      if speedright > 1:
         speedright = 1
      
      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      #printscreen()
      #return "Forward"

   # Accelerate backward
   elif (set_dist > (curr_dist + epsilon_dist) and set_dist < max_dist):
   #if(char == "s"):
      #print('backward')
      # Decrease duty cycle of all PWM pins by 10%
      #speedleft = speedleft - 0.01
      #speedright = speedright - 0.01
      speedleft = -0.35
      speedright = -0.35
      if speedleft < -1:
         speedleft = -1
      if speedright < -1:
         speedright = -1
              
      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      #printscreen()
      #return "Backward"

   # Move sideways to the right
   if(char == "y"):      
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
      #printscreen()

   # Move sideways to the left
   if(char == "c"):
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
      #printscreen()
      
   # Exit program
   if(char == "x"):
      HBridge.setMotorDirection("leftmotor_back", 0)
      HBridge.setMotorDirection("leftmotor_front", 0)
      HBridge.setMotorDirection("rightmotor_back", 0)
      HBridge.setMotorDirection("rightmotor_front", 0)  
      HBridge.exit()
      print("Program successfully ended")
   
   # Dumb variable char
   char = ""   
   return ""

def move2(remoteControl):
   global speedleft
   global speedright
   #char = getch()
   char = 'm'

   # Stop all motors
   if(remoteControl is None):
      #print("stopped")
      speedleft = 0
      speedright = 0
      HBridge.setMotorDirection("leftmotor_back", speedleft)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright)
      HBridge.setMotorDirection("rightmotor_front", speedright)  
      #printscreen()

   # Rotate right
   elif (remoteControl == 'd'):
      #print('right')
   #if (char == "d"):      
      #speedright = speedright - 0.1
      #speedleft = speedleft + 0.1
      speedright = -0.4
      speedleft = 0.4

      if speedright < -1:
         speedright = -1
      
      if speedleft > 1:
         speedleft = 1

      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)

   # Rotate left
   elif (remoteControl == 'a'):
      #print('left')
   #elif (char == "a"):
      #speedleft = speedleft - 0.1
      #speedright = speedright + 0.1
      speedright = 0.4
      speedleft = -0.4
         
      if speedleft < -1:
         speedleft = -1
      
      if speedright > 1:
         speedright = 1

      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      #printscreen()
      #printscreen()


   # Accelerate forward
   elif (remoteControl == 'w'):
   #if(char == "w"):
      #print('forward')
      # Increase duty cycle of all PWM pins by 10%
      #speedleft = speedleft + 0.01
      #speedright = speedright + 0.01
      speedleft = 0.3
      speedright = 0.3
      if speedleft > 1:
         speedleft = 1
      if speedright > 1:
         speedright = 1
      
      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      #printscreen()

   # Accelerate backward
   elif (remoteControl == 's'):
   #if(char == "s"):
      #print('backward')
      # Decrease duty cycle of all PWM pins by 10%
      #speedleft = speedleft - 0.01
      #speedright = speedright - 0.01
      speedleft = -0.3
      speedright = -0.3
      if speedleft < -1:
         speedleft = -1
      if speedright < -1:
         speedright = -1
              
      HBridge.setMotorDirection("leftmotor_back", speedleft*-1)
      HBridge.setMotorDirection("leftmotor_front", speedleft)
      HBridge.setMotorDirection("rightmotor_back", speedright*-1)
      HBridge.setMotorDirection("rightmotor_front", speedright)
      #printscreen()

   # Move sideways to the right
   if(char == "y"):      
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
      #printscreen()

   # Move sideways to the left
   if(char == "c"):
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
      #printscreen()
      
   # Exit program
   if(char == "x"):
      HBridge.setMotorDirection("leftmotor_back", 0)
      HBridge.setMotorDirection("leftmotor_front", 0)
      HBridge.setMotorDirection("rightmotor_back", 0)
      HBridge.setMotorDirection("rightmotor_front", 0)  
      HBridge.exit()
      print("Program successfully ended")
   
   # Dumb variable char
   char = ""
