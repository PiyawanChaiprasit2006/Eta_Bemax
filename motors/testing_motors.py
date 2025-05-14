# import time
# import RPi.GPIO as GPIO

# # Set up GPIO pins with BCM pin numbering
# GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering

# # Set up pins for motor control
# GPIO.setup(12, GPIO.OUT)  # Connected to ENA (PWMO)
# GPIO.setup(23, GPIO.OUT)  # Connected to IN1 (GPIO23 -> Pin 16)
# GPIO.setup(24, GPIO.OUT)  # Connected to IN2 (GPIO24 -> Pin 18)

# try:
#     print("Setting up PWM for speed control...")
#     pwm = GPIO.PWM(12, 1000)  # 1 kHz frequency
#     pwm.start(100)  # Start with 100% duty cycle (full speed)
    
#     print("Driving motor aclockwise for 5 seconds...")
#     GPIO.output(23, GPIO.HIGH)  # Set IN1 (GPIO23 -> Pin 16)
#     GPIO.output(24, GPIO.LOW)   # Set IN2 (GPIO24 -> Pin 18)
#     time.sleep(5)

#     print("Driving motor counterclockwise for 5 seconds...")
#     GPIO.output(23, GPIO.LOW)   # Set IN1 (GPIO23 -> Pin 16)
#     GPIO.output(24, GPIO.HIGH)  # Set IN2 (GPIO24 -> Pin 18)
#     time.sleep(5)

#     print("Stopping motor.")
#     pwm.ChangeDutyCycle(0)  # Set speed to 0

#     print(f"GPIO 24 state: {GPIO.input(24)}")

# finally:
#     print("Stopping PWM and cleaning up GPIO settings.")
#     pwm.stop()  # Stop the PWM properly
#     pwm = None  # Explicitly delete the PWM object
#     GPIO.cleanup()
#     print("GPIO cleaned up.")

import RPi.GPIO as GPIO
import time

# GPIO pin setup for Motor A
ENA = 18  # PWM pin
IN1 = 23
IN2 = 24

# GPIO pin setup for Motor B
ENB = 12  # PWM pin
IN3 = 17
IN4 = 27

# Motor B GPIO pin setup (Right Motor)
ENB = 12  # PWM pin
IN3 = 17  # GPIO17 -> Pin 11
IN4 = 27  # GPIO27 -> Pin 13

# GPIO settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup Motor A pins
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# Setup Motor B pins
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# PWM setup
pwmA = GPIO.PWM(ENA, 1000)  # Motor A at 1 kHz
pwmB = GPIO.PWM(ENB, 1000)  # Motor B at 1 kHz
pwmA.start(0)
pwmB.start(0)

try:
    # --- Test Motor A ---
    print("Motor A: clockwise")
    pwmA.ChangeDutyCycle(50)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(3)

    print("Motor A: stopped")
    pwmA.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(1)

    print("Motor A: counterclockwise")
    pwmA.ChangeDutyCycle(50)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    time.sleep(3)

    print("Motor A: stopped")
    pwmA.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    time.sleep(1)

    # --- Test Motor B ---
    print("Motor B: clockwise")
    pwmB.ChangeDutyCycle(50)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(3)

    print("Motor B: stopped")
    pwmB.ChangeDutyCycle(0)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    time.sleep(1)

    print("Motor B: counterclockwise")
    pwmB.ChangeDutyCycle(50)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    time.sleep(3)

    print("Motor B: stopped")
    pwmB.ChangeDutyCycle(0)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

finally:
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
    print("Cleanup complete.")

