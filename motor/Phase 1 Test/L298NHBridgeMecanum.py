#!/usr/bin/env python
# Adapted from Ingmar Stapel

import RPi.GPIO as io
io.setmode(io.BCM)

PWM_MAX = 70

io.setwarnings(False)

# ---------------------------------------------------------------------------- #
#                              GPIO Configuration                              #
# ---------------------------------------------------------------------------- #

# Back left motor
L_ENA = 4
L_IN1 = 17
L_IN2 = 18

# Front left motor
L_ENB = 23
L_IN3 = 24
L_IN4 = 25

# Right front motor
R_ENA = 20
R_IN1 = 12
R_IN2 = 16

# Right back motor
R_ENB = 26
R_IN3 = 19
R_IN4 = 13
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                               Motor Connections                              #
# ---------------------------------------------------------------------------- #

# -------------------------------- Left Motors ------------------------------- #

leftmotor_back_in1_pin = L_IN1
leftmotor_back_in2_pin = L_IN2
leftmotor_front_in1_pin = L_IN3
leftmotor_front_in2_pin = L_IN4

# Set L_IN1-4 as outputs
io.setup(leftmotor_back_in1_pin, io.OUT)
io.setup(leftmotor_back_in2_pin, io.OUT)
io.setup(leftmotor_front_in1_pin, io.OUT)
io.setup(leftmotor_front_in2_pin, io.OUT)

# Ensure that motors do not accidentally turn if enabled
io.output(leftmotor_back_in1_pin, False)
io.output(leftmotor_back_in2_pin, False)
io.output(leftmotor_front_in1_pin, False)
io.output(leftmotor_front_in2_pin, False)

# Define PWM pins 
leftmotorpwm_back_pin = L_ENA
leftmotorpwm_front_pin = L_ENB

# Configure PWM pins as outputs
io.setup(leftmotorpwm_back_pin, io.OUT)
io.setup(leftmotorpwm_front_pin, io.OUT)

# Configure each PWM pin with a frequency of 100 Hz
leftmotorpwm_back = io.PWM(leftmotorpwm_back_pin,100)
leftmotorpwm_front = io.PWM(leftmotorpwm_front_pin,100)

# Disable motors by setting their PWM pins with a 0% duty cycle
leftmotorpwm_back.start(0)
leftmotorpwm_front.start(0)

# ------------------------------- Right Motors ------------------------------- #

rightmotor_back_in1_pin = R_IN3
rightmotor_back_in2_pin = R_IN4
rightmotor_front_in1_pin = R_IN1
rightmotor_front_in2_pin = R_IN2

# Set R_IN1-4 as outputs
io.setup(rightmotor_back_in1_pin, io.OUT)
io.setup(rightmotor_back_in2_pin, io.OUT)
io.setup(rightmotor_front_in1_pin, io.OUT)
io.setup(rightmotor_front_in2_pin, io.OUT)

# Ensure that motors do not accidentally turn if enabled
io.output(rightmotor_back_in1_pin, False)
io.output(rightmotor_back_in2_pin, False)
io.output(rightmotor_front_in1_pin, False)
io.output(rightmotor_front_in2_pin, False)

# Define PWM pins
rightmotorpwm_back_pin = R_ENB
rightmotorpwm_front_pin = R_ENA

# Configure PWM pins as outputs
io.setup(rightmotorpwm_back_pin, io.OUT)
io.setup(rightmotorpwm_front_pin, io.OUT)

# Configure each PWM pin with a frequency of 100 Hz
rightmotorpwm_back = io.PWM(rightmotorpwm_back_pin,100)
rightmotorpwm_front = io.PWM(rightmotorpwm_front_pin,100)

# Disable motors by setting their PWM pins with a 0% duty cycle
rightmotorpwm_back.start(0)
rightmotorpwm_front.start(0)

# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                            Motor Control Functions                           #
# ---------------------------------------------------------------------------- #

def setMotorMode(motor, mode):
   if motor == "leftmotor_back":
      if mode == "reverse":
         io.output(leftmotor_back_in1_pin, False)
         io.output(leftmotor_back_in2_pin, True)
      elif  mode == "forward":
         io.output(leftmotor_back_in1_pin, True)
         io.output(leftmotor_back_in2_pin, False)
      else:
         io.output(leftmotor_back_in1_pin, False)
         io.output(leftmotor_back_in2_pin, False)
   elif motor == "leftmotor_front":
      if mode == "reverse":
         io.output(leftmotor_front_in1_pin, True)
         io.output(leftmotor_front_in2_pin, False)      
      elif  mode == "forward":
         io.output(leftmotor_front_in1_pin, False)
         io.output(leftmotor_front_in2_pin, True)
      else:
         io.output(leftmotor_front_in1_pin, False)
         io.output(leftmotor_front_in2_pin, False)
   elif motor == "rightmotor_back":
      if mode == "reverse":
         io.output(rightmotor_back_in1_pin, False)
         io.output(rightmotor_back_in2_pin, True)
      elif  mode == "forward":
         io.output(rightmotor_back_in1_pin, True)
         io.output(rightmotor_back_in2_pin, False)
      else:
         io.output(rightmotor_back_in1_pin, False)
         io.output(rightmotor_back_in2_pin, False)
   elif motor == "rightmotor_front":
      if mode == "reverse":
         io.output(rightmotor_front_in1_pin, True)
         io.output(rightmotor_front_in2_pin, False)      
      elif  mode == "forward":
         io.output(rightmotor_front_in1_pin, False)
         io.output(rightmotor_front_in2_pin, True)
      else:
         io.output(rightmotor_front_in1_pin, False)
         io.output(rightmotor_front_in2_pin, False)
   else:
      io.output(leftmotor_back_in1_pin, False)
      io.output(leftmotor_back_in2_pin, False)
      io.output(leftmotor_front_in1_pin, False)
      io.output(leftmotor_front_in2_pin, False)
	  
      io.output(rightmotor_back_in1_pin, False)
      io.output(rightmotor_back_in2_pin, False)
      io.output(rightmotor_front_in1_pin, False)
      io.output(rightmotor_front_in2_pin, False)

def setMotorDirection(motor, power):
   int(power)
   if power < 0:
      setMotorMode(motor, "reverse")
      pwm = -int(PWM_MAX * power)
      if pwm > PWM_MAX:
         pwm = PWM_MAX
   elif power > 0:
      setMotorMode(motor, "forward")
      pwm = int(PWM_MAX * power)
      if pwm > PWM_MAX:
         pwm = PWM_MAX
   else:
      setMotorMode(motor, "stop")
      pwm = 0
   
   if motor == "leftmotor_back":
      leftmotorpwm_back.ChangeDutyCycle(pwm)
   elif motor == "leftmotor_front":
      leftmotorpwm_front.ChangeDutyCycle(pwm)
   elif motor == "rightmotor_back":
      rightmotorpwm_back.ChangeDutyCycle(pwm)
   elif motor == "rightmotor_front":
      rightmotorpwm_front.ChangeDutyCycle(pwm) 
   else:
      exit()
   
# Disable motors and clear GPIO state
def exit():
   io.output(leftmotor_back_in1_pin, False)
   io.output(leftmotor_back_in2_pin, False)
   io.output(leftmotor_front_in1_pin, False)
   io.output(leftmotor_front_in2_pin, False)
   
   io.output(rightmotor_back_in1_pin, False)
   io.output(rightmotor_back_in2_pin, False)
   io.output(rightmotor_front_in1_pin, False)
   io.output(rightmotor_front_in2_pin, False) 
   io.cleanup()
   
# ---------------------------------------------------------------------------- #
