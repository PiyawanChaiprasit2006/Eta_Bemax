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

# GPIO pin setup
ENA = 18  # PWM pin (motor 1)
IN1 = 23  # GPIO23 -> Pin 16
IN2 = 24  # GPIO24 -> Pin 18

# GPIO settings
GPIO.setwarnings(False)  # Suppress warnings
GPIO.setmode(GPIO.BCM)   # Use BCM numbering

# Motor control pins setup
GPIO.setup(ENA, GPIO.OUT)  # ENA (PWM pin)
GPIO.setup(IN1, GPIO.OUT)  # IN1 (GPIO23 -> Pin 16)
GPIO.setup(IN2, GPIO.OUT)  # IN2 (GPIO24 -> Pin 18)

# PWM setup on ENA pin with 1 kHz frequency
pwm1 = GPIO.PWM(ENA, 1000)
pwm1.start(0)  # Start PWM with 0% duty cycle (stopped)

try:
    print("Testing motor direction...")

    # Clockwise rotation (IN1 HIGH, IN2 LOW)
    pwm1.ChangeDutyCycle(50)      # Set speed to 50%
    GPIO.output(IN1, GPIO.HIGH)   # Set IN1 (GPIO23 -> Pin 16)
    GPIO.output(IN2, GPIO.LOW)    # Set IN2 (GPIO24 -> Pin 18)
    print("Motor should rotate clockwise now...")
    time.sleep(3)

    # Stop motor between tests
    pwm1.ChangeDutyCycle(0)       # Stop PWM
    GPIO.output(IN1, GPIO.LOW)    # Set IN1 to LOW
    GPIO.output(IN2, GPIO.LOW)    # Set IN2 to LOW
    print("Motor stopped after clockwise rotation.")
    time.sleep(1)

    # Counterclockwise rotation (IN1 LOW, IN2 HIGH)
    pwm1.ChangeDutyCycle(50)      # Set speed to 50%
    GPIO.output(IN1, GPIO.LOW)    # Set IN1 (GPIO23 -> Pin 16)
    GPIO.output(IN2, GPIO.HIGH)   # Set IN2 (GPIO24 -> Pin 18)
    print("Motor should rotate counterclockwise now...")
    time.sleep(3)

    # Stop motor after counterclockwise test
    pwm1.ChangeDutyCycle(0)       # Stop PWM
    GPIO.output(IN1, GPIO.LOW)    # Set IN1 to LOW
    GPIO.output(IN2, GPIO.LOW)    # Set IN2 to LOW
    print("Motor stopped after counterclockwise rotation.")

finally:
    pwm1.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")
