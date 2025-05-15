# import numpy as np
# import cv2
# import RPi.GPIO as GPIO
# import time
# from collections import deque

# # === BCM pin defs ===
# ENA, IN1, IN2 = 18, 23, 24   # Motor 1: enable + dir+ + dir–
# ENB, IN3, IN4 = 12, 17, 27   # Motor 2: enable + dir+ + dir–

# # === GPIO Setup ===
# GPIO.setmode(GPIO.BCM)
# GPIO.setup((ENA, IN1, IN2, ENB, IN3, IN4), GPIO.OUT, initial=GPIO.LOW)

# pwm_a = GPIO.PWM(ENA, 1000)
# pwm_b = GPIO.PWM(ENB, 1000)
# pwm_a.start(0)
# pwm_b.start(0)

# # Motor speed control
# MOTOR_SPEED = 70  # Set motor speed (0-100%)

# # Distance estimation parameters
# KNOWN_HEIGHT = 1.7       # average person height (meters)
# FOCAL_LENGTH = 800       # tuned value for better accuracy
# STOP_DISTANCE = 0.3      # meters threshold to stop

# # Smoothing buffer
# distance_buffer = deque(maxlen=5)

# # Model paths
# prototxt = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.prototxt"
# caffe_model = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.caffemodel"
# net = cv2.dnn.readNetFromCaffe(prototxt, caffe_model)

# # Constants
# PERSON_CLASS_ID = 15

# # Video capture (V4L2 backend for stability)
# cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
# if not cap.isOpened():
#     print("Error: Cannot open camera")
#     exit()

# try:
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         h, w = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(frame, 1/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True)
#         net.setInput(blob)
#         detections = net.forward()

#         person_detected = False
#         bbox_height = None

#         # Process only the first detected person
#         for i in range(detections.shape[2]):
#             conf = detections[0, 0, i, 2]
#             class_id = int(detections[0, 0, i, 1])
#             if conf > 0.5 and class_id == PERSON_CLASS_ID:
#                 person_detected = True
#                 box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                 x1, y1, x2, y2 = box.astype(int)
#                 bbox_height = y2 - y1
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 break

#         # Estimate and smooth distance
#         if bbox_height and bbox_height > 0:
#             distance = (FOCAL_LENGTH * KNOWN_HEIGHT) / bbox_height
#             distance_buffer.append(distance)
#             avg_distance = sum(distance_buffer) / len(distance_buffer)
#             cv2.putText(frame, f"Dist: {avg_distance:.2f}m", (10, 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
#         else:
#             avg_distance = None

#         # Motor control
#         if person_detected and avg_distance is not None:
#             if avg_distance <= STOP_DISTANCE:
#                 pwm_a.ChangeDutyCycle(0)
#                 pwm_b.ChangeDutyCycle(0)
#             else:
#                 center_x = (x1 + x2) // 2
#                 pwm_a.ChangeDutyCycle(MOTOR_SPEED)
#                 pwm_b.ChangeDutyCycle(MOTOR_SPEED)
#                 if center_x < w * 0.4:
#                     GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.HIGH)
#                     GPIO.output(IN3, GPIO.HIGH); GPIO.output(IN4, GPIO.LOW)
#                 elif center_x > w * 0.6:
#                     GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
#                     GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.HIGH)
#                 else:
#                     GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
#                     GPIO.output(IN3, GPIO.HIGH); GPIO.output(IN4, GPIO.LOW)
#         else:
#             pwm_a.ChangeDutyCycle(0)
#             pwm_b.ChangeDutyCycle(0)

#         cv2.imshow("Human Tracking", frame)
#         if cv2.waitKey(1) == 27:
#             break

# finally:
#     pwm_a.stop()
#     pwm_b.stop()
#     GPIO.cleanup()
#     cap.release()
#     cv2.destroyAllWindows()

import numpy as np
import cv2

import RPi.GPIO as GPIO
import time

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
MOTOR_SPEED = 70  # Set motor speed (0-100%)

# Path to the prototxt file and the caffemodel (Linux-style paths)
prototxt = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.prototxt"
caffe_model = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.caffemodel"
# Load the model
net = cv2.dnn.readNetFromCaffe(prototxt, caffe_model)

# Class labels
classNames = {15: 'person'}

# Known real-world object heights (in meters)
KNOWN_HEIGHTS = {"person": 1.7}

# Estimated focal length (adjust after calibration)
FOCAL_LENGTH = 615

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot open camera")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width = frame.shape[:2]

        # Preprocess image
        blob = cv2.dnn.blobFromImage(frame, 1/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True)
        net.setInput(blob)
        detections = net.forward()

        person_detected = False

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])
                if class_id == 15:
                    person_detected = True
                    x1, y1 = int(detections[0, 0, i, 3] * width), int(detections[0, 0, i, 4] * height)
                    x2, y2 = int(detections[0, 0, i, 5] * width), int(detections[0, 0, i, 6] * height)

                    bbox_height = y2 - y1
                    distance = (FOCAL_LENGTH * KNOWN_HEIGHTS["person"]) / bbox_height if bbox_height > 0 else None

                    if distance and distance <= 0.3:
                        print("Stopping")
                        pwm_a.ChangeDutyCycle(0)
                        pwm_b.ChangeDutyCycle(0)
                    else:
                        center_x = (x1 + x2) // 2
                        if center_x < width * 0.4:
                            print("Turning Left")
                            pwm_a.ChangeDutyCycle(MOTOR_SPEED)
                            pwm_b.ChangeDutyCycle(MOTOR_SPEED)
                            GPIO.output(IN1, GPIO.LOW)
                            GPIO.output(IN2, GPIO.HIGH)
                            GPIO.output(IN3, GPIO.HIGH)
                            GPIO.output(IN4, GPIO.LOW)
                        elif center_x > width * 0.6:
                            print("Turning Right")
                            pwm_a.ChangeDutyCycle(MOTOR_SPEED)
                            pwm_b.ChangeDutyCycle(MOTOR_SPEED)
                            GPIO.output(IN1, GPIO.HIGH)
                            GPIO.output(IN2, GPIO.LOW)
                            GPIO.output(IN3, GPIO.LOW)
                            GPIO.output(IN4, GPIO.HIGH)
                        else:
                            print("Moving Forward")
                            pwm_a.ChangeDutyCycle(MOTOR_SPEED)
                            pwm_b.ChangeDutyCycle(MOTOR_SPEED)
                            GPIO.output(IN1, GPIO.HIGH)
                            GPIO.output(IN2, GPIO.LOW)
                            GPIO.output(IN3, GPIO.HIGH)
                            GPIO.output(IN4, GPIO.LOW)

        if not person_detected:
            print("No person detected. Stopping.")
            pwm_a.ChangeDutyCycle(0)
            pwm_b.ChangeDutyCycle(0)

        cv2.imshow("Object Detection with Distance", frame)
        if cv2.waitKey(1) == 27:  # Press ESC to quit
            break

finally:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()

