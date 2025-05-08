# import RPi.GPIO as GPIO
# import time

# # Pin setup (can adjust)
# IN1 = 1  # Left motor forward
# IN2 = 27  # Left motor backward
# IN3 = 23  # Right motor forward
# IN4 = 24  # Right motor backward
# ENA = 22  # Left motor enable (PWM)
# ENB = 25  # Right motor enable (PWM)

# GPIO.setmode(GPIO.BCM)
# GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)

# pwm_left = GPIO.PWM(ENA, 1000)
# pwm_right = GPIO.PWM(ENB, 1000)
# pwm_left.start(0)
# pwm_right.start(0)

# speed=80

# if button == pressed:
#         time.sleep(0.5)

# def mforward():
#     if button == pressed:
#         time.sleep(0.5)
#     while button == pressed:
#         GPIO.output(IN1, GPIO.HIGH)
#         GPIO.output(IN2, GPIO.LOW)
#         GPIO.output(IN3, GPIO.HIGH)
#         GPIO.output(IN4, GPIO.LOW)
#         pwm_left.ChangeDutyCycle(speed)
#         pwm_right.ChangeDutyCycle(speed)
    

# def mleft():
#     if button == pressed:
#         time.sleep(0.5)
#     while button == pressed:
#         GPIO.output(IN1, GPIO.LOW)
#         GPIO.output(IN2, GPIO.HIGH)
#         GPIO.output(IN3, GPIO.HIGH)
#         GPIO.output(IN4, GPIO.LOW)
#         pwm_left.ChangeDutyCycle(speed)
#         pwm_right.ChangeDutyCycle(speed)
    
# def mright():
#     if button == pressed:
#         time.sleep(0.5)
#     while button == pressed:
#         GPIO.output(IN1, GPIO.HIGH)
#         GPIO.output(IN2, GPIO.LOW)
#         GPIO.output(IN3, GPIO.LOW)
#         GPIO.output(IN4, GPIO.HIGH)
#         pwm_left.ChangeDutyCycle(speed)
#         pwm_right.ChangeDutyCycle(speed)

# def mbackward():
#     if button == pressed:
#         time.sleep(0.1)
#     while button == pressed:
#         GPIO.output(IN1, GPIO.LOW)
#         GPIO.output(IN2, GPIO.HIGH)
#         GPIO.output(IN3, GPIO.LOW)
#         GPIO.output(IN4, GPIO.HIGH)
#         pwm_left.ChangeDutyCycle(speed)
#         pwm_right.ChangeDutyCycle(speed)

# def stop():
#     GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
#     pwm_left.ChangeDutyCycle(0)
#     pwm_right.ChangeDutyCycle(0)

