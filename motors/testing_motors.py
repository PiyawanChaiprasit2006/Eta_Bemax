import time
import RPi.GPIO as GPIO

# Set up GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)  # Connected to PWMO
GPIO.setup(16, GPIO.OUT)  # Connected to GPIO23 (AIN1)
GPIO.setup(18, GPIO.OUT)  # Connected to GPIO24 (AIN2)
GPIO.setup(2, GPIO.OUT)   # 5V Power (already constant)
GPIO.setup(6, GPIO.OUT)   # GND (already constant)

# Drive the motor clockwise
GPIO.output(16, GPIO.HIGH)  # Set GPIO23 (AIN1)
GPIO.output(18, GPIO.LOW)   # Set GPIO24 (AIN2)
GPIO.output(12, GPIO.HIGH)  # Set PWMO

# Wait 5 seconds
time.sleep(5)

# Drive the motor counterclockwise
GPIO.output(16, GPIO.LOW)   # Set GPIO23 (AIN1)
GPIO.output(18, GPIO.HIGH)  # Set GPIO24 (AIN2)
GPIO.output(12, GPIO.HIGH)  # Set PWMO

# Wait 5 seconds
time.sleep(5)

# Reset all the GPIO pins by setting them to LOW
GPIO.output(16, GPIO.LOW)
GPIO.output(18, GPIO.LOW)
GPIO.output(12, GPIO.LOW)

# Clean up GPIO settings
GPIO.cleanup()
