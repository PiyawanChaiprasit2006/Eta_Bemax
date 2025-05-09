import time
import RPi.GPIO as GPIO

# Set up GPIO pins with BCM pin numbering
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering

# Set up pins for motor control
GPIO.setup(12, GPIO.OUT)  # Connected to ENA (PWMO)
GPIO.setup(23, GPIO.OUT)  # Connected to IN1 (GPIO23 -> Pin 16)
GPIO.setup(24, GPIO.OUT)  # Connected to IN2 (GPIO24 -> Pin 18)

pwm = None  # Initialize PWM variable

try:
    print("Setting up PWM for speed control...")
    pwm = GPIO.PWM(12, 1000)  # 1 kHz frequency
    pwm.start(75)  # Start with 75% duty cycle for safer testing
    
    print("Driving motor clockwise for 5 seconds...")
    GPIO.output(23, GPIO.HIGH)  # Set IN1 (GPIO23 -> Pin 16)
    GPIO.output(24, GPIO.LOW)   # Set IN2 (GPIO24 -> Pin 18)
    time.sleep(5)

    print("Driving motor counterclockwise for 5 seconds...")
    GPIO.output(23, GPIO.LOW)   # Set IN1 (GPIO23 -> Pin 16)
    GPIO.output(24, GPIO.HIGH)  # Set IN2 (GPIO24 -> Pin 18)
    time.sleep(5)

    print("Stopping motor.")
    pwm.ChangeDutyCycle(0)  # Set speed to 0

    print(f"GPIO 23 state: {GPIO.input(23)}")
    print(f"GPIO 24 state: {GPIO.input(24)}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("Stopping PWM and cleaning up GPIO settings.")
    if pwm:
        pwm.stop()  # Stop the PWM properly
    GPIO.cleanup()
    print("GPIO cleaned up.")
