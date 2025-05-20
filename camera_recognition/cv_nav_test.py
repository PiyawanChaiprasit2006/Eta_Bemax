import numpy as np
import cv2
import RPi.GPIO as GPIO
import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# === BCM pin defs ===
ENA, IN1, IN2 = 18, 23, 24   # Motor 1: enable + dir+ + dir–
ENB, IN3, IN4 = 12, 17, 27   # Motor 2: enable + dir+ + dir–

# === GPIO Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup((ENA, IN1, IN2, ENB, IN3, IN4), GPIO.OUT, initial=GPIO.LOW)

pwm_a = GPIO.PWM(ENA, 1000)
pwm_b = GPIO.PWM(ENB, 1000)
pwm_a.start(0)
pwm_b.start(0)

# === Servo Setup ===
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz for SG90 servos

def angle_to_duty(angle):
    min_us = 500    # 0° = 500 microseconds
    max_us = 2500   # 180° = 2500 microseconds
    pulse_us = min_us + (angle / 180.0) * (max_us - min_us)
    duty = int(pulse_us * 65535 / (1000000 / pca.frequency))
    return duty

def open_and_close_servos():
    for channel in range(4):
        pca.channels[channel].duty_cycle = angle_to_duty(90)  # Open
    time.sleep(30)
    for channel in range(4):
        pca.channels[channel].duty_cycle = angle_to_duty(0)  # Close

MOTOR_SPEED = 70
prototxt = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.prototxt"
caffe_model = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.caffemodel"

net = cv2.dnn.readNetFromCaffe(prototxt, caffe_model)
classNames = {15: 'person'}
KNOWN_HEIGHTS = {"person": 1.7}
FOCAL_LENGTH = 615

def estimate_distance(height_in_frame):
    if height_in_frame == 0:
        return float('inf')
    return (KNOWN_HEIGHTS["person"] * FOCAL_LENGTH) / height_in_frame

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot open camera")
    exit()

try:
    start_time = time.time()
    person_found = False

    while time.time() - start_time < 6:
        print("Spinning to search for a person...")
        pwm_a.ChangeDutyCycle(MOTOR_SPEED)
        pwm_b.ChangeDutyCycle(MOTOR_SPEED)
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)

        ret, frame = cap.read()
        if not ret:
            break

        if cv2.waitKey(1) == 27:  # ESC to quit
            raise KeyboardInterrupt

        blob = cv2.dnn.blobFromImage(frame, 1/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True)
        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5 and int(detections[0, 0, i, 1]) == 15:
                person_found = True
                print("Person detected!")
                pwm_a.ChangeDutyCycle(0)
                pwm_b.ChangeDutyCycle(0)
                break

        if person_found:
            break

    if person_found:
        print("Centering on the person...")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if cv2.waitKey(1) == 27:  # ESC to quit
                raise KeyboardInterrupt

            height, width = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(frame, 1/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True)
            net.setInput(blob)
            detections = net.forward()

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5 and int(detections[0, 0, i, 1]) == 15:
                    box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                    x1, y1, x2, y2 = box.astype("int")
                    center_x = (x1 + x2) // 2
                    person_height = y2 - y1
                    distance = estimate_distance(person_height)

                    print(f"Estimated distance: {distance:.2f} meters")
                    frame_center = width // 2

                    if distance <= 2.2:
                        print("Reached target distance. Stopping.")
                        pwm_a.ChangeDutyCycle(0)
                        pwm_b.ChangeDutyCycle(0)
                        open_and_close_servos()
                        raise KeyboardInterrupt

                    if center_x < frame_center - 30:
                        print("Adjusting Right")
                        GPIO.output(IN1, GPIO.HIGH)
                        GPIO.output(IN2, GPIO.LOW)
                        GPIO.output(IN3, GPIO.LOW)
                        GPIO.output(IN4, GPIO.HIGH)
                    elif center_x > frame_center + 30:
                        print("Adjusting Left")
                        GPIO.output(IN1, GPIO.LOW)
                        GPIO.output(IN2, GPIO.HIGH)
                        GPIO.output(IN3, GPIO.HIGH)
                        GPIO.output(IN4, GPIO.LOW)
                    else:
                        print("Centered. Moving Forward.")
                        pwm_a.ChangeDutyCycle(MOTOR_SPEED)
                        pwm_b.ChangeDutyCycle(MOTOR_SPEED)
                        GPIO.output(IN1, GPIO.LOW)
                        GPIO.output(IN2, GPIO.HIGH)
                        GPIO.output(IN3, GPIO.LOW)
                        GPIO.output(IN4, GPIO.HIGH)

finally:
    print("Cleaning up...")
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
