try:
    import RPi.GPIO as GPIO
except (ImportError, ModuleNotFoundError):
    from mocks.RPi import GPIO  # Use mock GPIO if running locally
import time

# GPIO settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Motor A GPIO pin setup (Left Motor)
ENA = 18  # PWM pin
IN1 = 23  # GPIO23 -> Pin 16
IN2 = 24  # GPIO24 -> Pin 18

# Motor B GPIO pin setup (Right Motor)
ENB = 12  # PWM pin
IN3 = 17  # GPIO17 -> Pin 11
IN4 = 27  # GPIO27 -> Pin 13

# Motor control pins setup
motor_pins = [(ENA, IN1, IN2), (ENB, IN3, IN4)]

for ena, in1, in2 in motor_pins:
    GPIO.setup(ena, GPIO.OUT)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)

# PWM setup for both motors
pwmA = GPIO.PWM(ENA, 1000)
pwmB = GPIO.PWM(ENB, 1000)
pwmA.start(0)
pwmB.start(0)

# Motor control functions
def stop_motors():
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def move_forward(speed=50):
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def move_backward(speed=50):
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def turn_right(speed=50):
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def turn_left(speed=50):
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def cleanup():
    stop_motors()
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")
