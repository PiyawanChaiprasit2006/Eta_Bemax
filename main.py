import numpy as np
import cv2
import RPi.GPIO as GPIO
import time
from collections import deque

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

# Motor speed control
MOTOR_SPEED = 50  # Set motor speed (0-100%)

# Distance estimation parameters
KNOWN_HEIGHT = 1.7       # average person height (meters)
FOCAL_LENGTH = 800       # tuned value for better accuracy
STOP_DISTANCE = 0.3      # meters threshold to stop

# Smoothing buffer
distance_buffer = deque(maxlen=5)

# Model paths
prototxt = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.prototxt"
caffe_model = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototxt, caffe_model)

# Constants
PERSON_CLASS_ID = 15

def spin_in_place(speed=70):
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)
    GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)  # Motor 1 forward
    GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.HIGH)  # Motor 2 backward

def stop_motors():
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

def move_towards_person(direction="forward"):
    pwm_a.ChangeDutyCycle(MOTOR_SPEED)
    pwm_b.ChangeDutyCycle(MOTOR_SPEED)
    
    if direction == "left":
        GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH); GPIO.output(IN4, GPIO.LOW)
    elif direction == "right":
        GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.HIGH)
    else:  # forward
        GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH); GPIO.output(IN4, GPIO.LOW)

# Video capture (V4L2 backend for stability)
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
if not cap.isOpened():
    print("Error: Cannot open camera")
    exit()

spinning = True  # Flag to control spinning

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True)
        net.setInput(blob)
        detections = net.forward()

        person_detected = False
        bbox_height = None

        for i in range(detections.shape[2]):
            conf = detections[0, 0, i, 2]
            class_id = int(detections[0, 0, i, 1])
            if conf > 0.5 and class_id == PERSON_CLASS_ID:
                person_detected = True
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                x1, y1, x2, y2 = box.astype(int)
                bbox_height = y2 - y1
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                break

        if person_detected:
            spinning = False  # Stop spinning if person detected
            
            if bbox_height and bbox_height > 0:
                distance = (FOCAL_LENGTH * KNOWN_HEIGHT) / bbox_height
                distance_buffer.append(distance)
                avg_distance = sum(distance_buffer) / len(distance_buffer)
            else:
                avg_distance = None

            if avg_distance is not None and avg_distance <= STOP_DISTANCE:
                stop_motors()
                print("Stopping - Object too close")
            else:
                center_x = (x1 + x2) // 2
                if center_x < w * 0.4:
                    print("Turning Left")
                    move_towards_person("left")
                elif center_x > w * 0.6:
                    print("Turning Right")
                    move_towards_person("right")
                else:
                    print("Moving Straight")
                    move_towards_person("forward")
        else:
            if spinning:
                print("Spinning in place...")
                spin_in_place()
            else:
                stop_motors()

        cv2.imshow("Human Tracking", frame)
        if cv2.waitKey(1) == 27:
            break

finally:
    stop_motors()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()