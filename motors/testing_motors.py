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

import time
import RPi.GPIO as GPIO

# Set up GPIO pins with BCM pin numbering
GPIO.setmode(GPIO.BCM)

ENA = 18 # PWN pin (motor 1)
IN1 = 23 # GPIO23 -> Pin 16
IN2 = 24 # GPIO24 -> Pin 18

# Motor control pins
GPIO.setup(ENA, GPIO.OUT)  # ENA (PWM pin)
GPIO.setup(IN1, GPIO.OUT)  # IN1 (GPIO23 -> Pin 16)
GPIO.setup(IN2, GPIO.OUT)  # IN2 (GPIO24 -> Pin 18)

pwm1 = GPIO.PWN(ENA, 1000) # 1kHz PWN
pwm1.start(0) # Start at 0% (stopped)

try:
    print("Testing motor direction...")

    # Test clockwise rotation (IN1 HIGH, IN2 LOW)
    GPIO.output(IN1, GPIO.HIGH)  # Set IN1 (GPIO23 -> Pin 16)
    GPIO.output(IN2, GPIO.LOW)   # Set IN2 (GPIO24 -> Pin 18)
    for dc in range(0, 101, 10): # should slowly increase the speed of the motor
        pwm1.ChangeDutyCycle(dc)
        time.sleep(0.2)
    print("Motor should rotate clockwise now...")
    time.sleep(3)

    # Test counterclockwise rotation (IN1 LOW, IN2 HIGH)
    GPIO.output(IN1, GPIO.LOW)   # Set IN1 (GPIO23 -> Pin 16)
    GPIO.output(IN2, GPIO.HIGH)  # Set IN2 (GPIO24 -> Pin 18)
    for dc in range(0, 101, 10): # should slowly increase the speed of the motor
        pwm1.ChangeDutyCycle(dc)
        time.sleep(0.2)
    print("Motor should rotate counterclockwise now...")
    time.sleep(3)

finally:
    pwm1.stop()
    GPIO.cleanup()  # Clean up GPIO settings
    print("GPIO cleaned up.")
