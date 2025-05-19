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
MOTOR_SPEED = 50  # Set motor speed (0-100%)

# Path to the prototxt file and the caffemodel (Linux-style paths)
prototxt = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.prototxt"
caffe_model = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.caffemodel"

# Load the model
net = cv2.dnn.readNetFromCaffe(prototxt, caffe_model)

# Class labels
classNames = {15: 'person'}

# Known real-world object heights (in meters)
KNOWN_HEIGHTS = {"person": 1.7}
FOCAL_LENGTH = 615  # Estimated focal length (adjust after calibration)

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot open camera")
    exit()

# Function to spin in place
def spin_in_place(speed=70):
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

try:
    print("Spinning in place for up to 5 seconds to look for a person...")
    start_time = time.time()
    
    person_found = False

    # Spin for 5 seconds max
    while time.time() - start_time < 10:
        spin_in_place(MOTOR_SPEED)
        ret, frame = cap.read()
        if not ret:
            break

        # Process image to look for a person
        blob = cv2.dnn.blobFromImage(frame, 1/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True)
        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])
                if class_id == 15:
                    person_found = True
                    print("Person detected! Moving towards them...")
                    pwm_a.ChangeDutyCycle(0)
                    pwm_b.ChangeDutyCycle(0)
                    break
        
        if person_found:
            break

    # Stop spinning after 5 seconds or if person is found
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

    if person_found:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            height, width = frame.shape[:2]

            # Process image
            blob = cv2.dnn.blobFromImage(frame, 1/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True)
            net.setInput(blob)
            detections = net.forward()

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    class_id = int(detections[0, 0, i, 1])
                    if class_id == 15:
                        x1, y1 = int(detections[0, 0, i, 3] * width), int(detections[0, 0, i, 4] * height)
                        x2, y2 = int(detections[0, 0, i, 5] * width), int(detections[0, 0, i, 6] * height)

                        bbox_height = y2 - y1
                        distance = (FOCAL_LENGTH * KNOWN_HEIGHTS["person"]) / bbox_height if bbox_height > 0 else None
                        print(f"Person detected at {distance:.2f} meters.")

                        if distance and distance <= 0.3:
                            print("Stopping. Person is close enough.")
                            pwm_a.ChangeDutyCycle(0)
                            pwm_b.ChangeDutyCycle(0)
                        else:
                            print("Moving Forward")
                            pwm_a.ChangeDutyCycle(MOTOR_SPEED)
                            pwm_b.ChangeDutyCycle(MOTOR_SPEED)
                            GPIO.output(IN1, GPIO.LOW)
                            GPIO.output(IN2, GPIO.HIGH)
                            GPIO.output(IN3, GPIO.LOW)
                            GPIO.output(IN4, GPIO.HIGH)
                        break

            cv2.imshow("Object Detection with Distance", frame)
            if cv2.waitKey(1) == 27:  # ESC to quit
                break
    else:
        print("No person detected after 5 seconds.")

finally:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
