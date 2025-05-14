import time
import RPi.GPIO as GPIO

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(13, GPIO.OUT)  # ENA (PWM Control)
GPIO.setup(23, GPIO.OUT)  # IN1 (Motor Direction)
GPIO.setup(24, GPIO.OUT)  # IN2 (Motor Direction)

pwm = None  # Initialize PWM variable

try:
    print("Initializing motor control...")
    GPIO.output(23, GPIO.LOW)  # Ensure motor is stopped
    GPIO.output(24, GPIO.LOW)

    print("Setting up PWM on ENA (GPIO 18)...")
    pwm = GPIO.PWM(13, 1000)  # 1 kHz frequency
    pwm.start(0)  # Start with 0% duty cycle (motor stopped)

    print("\nDriving motor clockwise at 50% speed...")
    GPIO.output(23, GPIO.HIGH)  # IN1 HIGH
    GPIO.output(24, GPIO.LOW)   # IN2 LOW
    pwm.ChangeDutyCycle(50)     # 50% speed
    time.sleep(5)

    print("\nChanging speed to 75%...")
    pwm.ChangeDutyCycle(75)     # 75% speed
    time.sleep(5)

    print("\nStopping motor...")
    pwm.ChangeDutyCycle(0)  # Stop motor
    time.sleep(2)

    print("\nDriving motor counterclockwise at 50% speed...")
    GPIO.output(23, GPIO.LOW)   # IN1 LOW
    GPIO.output(24, GPIO.HIGH)  # IN2 HIGH
    pwm.ChangeDutyCycle(50)     # 50% speed
    time.sleep(5)

    print("\nStopping motor...")
    pwm.ChangeDutyCycle(0)  # Stop motor

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("\nCleaning up GPIO settings.")
    if pwm:
        pwm.stop()  # Stop the PWM properly
    GPIO.cleanup()
    print("GPIO cleaned up.")
