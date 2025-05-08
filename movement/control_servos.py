from gpiozero import Servo, Button
from signal import pause
from time import sleep

# Initialize servos (adjust min_pulse_width and max_pulse_width if needed)
servo1 = Servo(17, min_pulse_width = 1/1000, max_pulse_width = 2/1000)
servo2 = Servo(18, min_pulse_width = 1/1000, max_pulse_width = 2/1000)
servo3 = Servo(22, min_pulse_width = 1/1000, max_pulse_width = 2/1000)
servo4 = Servo(23, min_pulse_width = 1/1000, max_pulse_width = 2/1000)

# in order of 1, 2, 3, 4: burn, cut, eyes, treats
# min_pulse_width = 1/1000  # 1 ms
# max_pulse_width = 2/1000  # 2 ms

# initialize servo states to closed
servo_button1 = "closed"
servo_button2 = "closed"
servo_button3 = "closed"
servo_button4 = "closed"

# burn
def servo1():
    # if button is clicked, then if statements to determine state of servo
    if servo_button1 == "closed":
        #print("Servo 1 open")
        servo1.max()
        sleep(0.5)
        servo_button1 = "open"
    elif servo_button1 == "open":
        servo1.min()
        sleep(0.5)
        servo_button1 = "closed"

# cut
def servo2():
    # if button is clicked, then if statements to determine state of servo
    if servo_button2 == "closed":
        #print("Servo 2 open")
        servo2.max()
        sleep(0.5)
        servo_button2 = "open"
    elif servo_button2 == "open":
        servo2.min()
        sleep(0.5)
        servo_button2 = "closed"

# eyes
def servo3():
    # if button is clicked, then if statements to determine state of servo
    if servo_button3 == "closed":
        #print("Servo 3 open")
        servo3.max()
        sleep(0.5)
        servo_button3 = "open"
    elif servo_button3 == "open":
        servo3.min()
        sleep(0.5)
        servo_button3 = "closed"

# treats
def servo4():
    # if button is clicked, then if statements to determine state of servo
    if servo_button4 == "closed":
        #print("Servo 4 open")
        servo4.max()
        sleep(0.5)
        servo_button4 = "open"
    elif servo_button4 == "open":
        servo4.min()
        sleep(0.5)
        servo_button4 = "closed"