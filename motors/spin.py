import numpy as np
import cv2
import RPi.GPIO as GPIO
import time
from collections import deque

# === BCM pin defs ===
ENA, IN1, IN2 = 18, 23, 24   # Motor 1: enable + dir+ + dir–
ENB, IN3, IN4 = 12, 17, 27   # Motor 2: enable + dir+ + dir–

# === GPIO Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup((ENA, IN1, IN2, ENB, IN3, IN4), GPIO.OUT, initial=GPIO.LOW)

pwm_a = GPIO.PWM(ENA, 1000)
pwm_b = GPIO.PWM(ENB, 1000)
pwm_a.start(0)
pwm_b.start(0)

# Motor speed control
MOTOR_SPEED = 70  # Set motor speed (0-100%)

# Function to spin the robot in place
def spin_in_place(speed=70, duration=2):
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)

    # One motor forward, one backward
    GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)  # Motor 1 forward
    GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.HIGH)  # Motor 2 backward

    time.sleep(duration)

    # Stop motors
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

try:
    print("Spinning in place...")
    spin_in_place(speed=MOTOR_SPEED, duration=5)  # Spin for 5 seconds

finally:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
