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

# Path to the prototxt file and the caffemodel (Linux-style paths)
prototxt = "Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.prototxt"
caffe_model = "Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.caffemodel"

# Load the model
net = cv2.dnn.readNetFromCaffe(prototxt, caffe_model)

# Class labels
classNames = {0: 'background', 1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat', 5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair', 10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse', 14: 'motorbike', 15: 'person'}

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
                if class_id in classNames and classNames[class_id] == "person":
                    print("Person detected. Moving Forward.")
                    GPIO.output(ENA, GPIO.HIGH)
                    GPIO.output(IN1, GPIO.HIGH)
                    GPIO.output(IN2, GPIO.LOW)
                    GPIO.output(ENB, GPIO.HIGH)
                    GPIO.output(IN3, GPIO.HIGH)
                    GPIO.output(IN4, GPIO.LOW)
                    person_detected = True

        # If no person is detected, stop
        if not person_detected:
            GPIO.output(ENA, GPIO.LOW)
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(ENB, GPIO.LOW)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.LOW)

        cv2.imshow("Object Detection with Distance", frame)
        if cv2.waitKey(1) == 27:  # Press ESC to quit
            break

finally:
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
