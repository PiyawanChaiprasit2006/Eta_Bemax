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

# Motor control pins
GPIO.setup(12, GPIO.OUT)  # ENA (PWM pin)
GPIO.setup(23, GPIO.OUT)  # IN1 (GPIO23 -> Pin 16)
GPIO.setup(24, GPIO.OUT)  # IN2 (GPIO24 -> Pin 18)

try:
    print("Testing motor direction...")

    # Test clockwise rotation (IN1 HIGH, IN2 LOW)
    GPIO.output(23, GPIO.HIGH)  # Set IN1 (GPIO23 -> Pin 16)
    GPIO.output(24, GPIO.LOW)   # Set IN2 (GPIO24 -> Pin 18)
    print("Motor should rotate clockwise now...")
    time.sleep(3)

    # Test counterclockwise rotation (IN1 LOW, IN2 HIGH)
    GPIO.output(23, GPIO.LOW)   # Set IN1 (GPIO23 -> Pin 16)
    GPIO.output(24, GPIO.HIGH)  # Set IN2 (GPIO24 -> Pin 18)
    print("Motor should rotate counterclockwise now...")
    time.sleep(3)

finally:
    GPIO.cleanup()  # Clean up GPIO settings
    print("GPIO cleaned up.")
