
import time
import RPi.GPIO as GPIO

# Set up GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT) # Connected to PWMA
GPIO.setup(11, GPIO.OUT) # Connected to AIN2
GPIO.setup(12, GPIO.OUT) # Connected to AIN1
GPIO.setup(13, GPIO.OUT) # Connected to STBY

# Drive the motor clockwise
GPIO.output(12, GPIO.HIGH) # Set AIN1
GPIO.output(11, GPIO.LOW) # Set AIN2
GPIO.output(7, GPIO.HIGH) # Set PWMA
GPIO.output(13, GPIO.HIGH) # Disable STBY

# Wait 5 seconds
time.sleep(5)

# Drive the motor counterclockwise
GPIO.output(12, GPIO.LOW) # Set AIN1
GPIO.output(11, GPIO.HIGH) # Set AIN2
GPIO.output(7, GPIO.HIGH) # Set PWMA
GPIO.output(13, GPIO.HIGH) # Disable STBY

# Wait 5 seconds
time.sleep(5)

# Reset all the GPIO pins by setting them to LOW
GPIO.output(12, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
GPIO.output(7, GPIO.LOW)
GPIO.output(13, GPIO.LOW)

# Clean up GPIO settings
GPIO.cleanup()