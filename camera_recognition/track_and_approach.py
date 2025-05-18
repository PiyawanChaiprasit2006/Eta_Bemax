#!/usr/bin/env python3
import numpy as np
import cv2
import RPi.GPIO as GPIO
import time

# === BCM pin defs ===
ENA, IN1, IN2 = 18, 23, 24   # Motor 1: enable + dir+ + dir–
ENB, IN3, IN4 = 12, 17, 27   # Motor 2: enable + dir+ + dir–

# === Parameters ===
MOTOR_SPEED    = 50      # PWM duty cycle (0–100%)
STOP_DISTANCE  = 0.3     # meters
KNOWN_HEIGHT   = 1.7     # m (average person height)
FOCAL_LENGTH   = 615     # camera focal length (tune if needed)
CONF_THRESHOLD = 0.5     # detection confidence

# === Load DNN model ===
proto_path = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.prototxt"
model_path = "/home/piyawan/Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.caffemodel"
net = cv2.dnn.readNetFromCaffe(proto_path, model_path)

# === GPIO setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup((ENA, IN1, IN2, ENB, IN3, IN4), GPIO.OUT, initial=GPIO.LOW)
pwm_a = GPIO.PWM(ENA, 1000); pwm_b = GPIO.PWM(ENB, 1000)
pwm_a.start(0); pwm_b.start(0)

def spin(speed):
    """Rotate in place (M1 forward, M2 backward)."""
    pwm_a.ChangeDutyCycle(speed)
    pwm_b.ChangeDutyCycle(speed)
    GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW);  GPIO.output(IN4, GPIO.HIGH)

def stop():
    """Brake both motors."""
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)

def detect_person(frame):
    """
    Run SSD on the frame. If a person (class 15) is found,
    return (True, distance, center_x). Else (False, None, None).
    """
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1/127.5, (300,300),
                                 (127.5,127.5,127.5), swapRB=True)
    net.setInput(blob)
    dets = net.forward()

    for i in range(dets.shape[2]):
        conf = dets[0,0,i,2]
        cls  = int(dets[0,0,i,1])
        if conf > CONF_THRESHOLD and cls == 15:
            x1 = int(dets[0,0,i,3]*w)
            y1 = int(dets[0,0,i,4]*h)
            x2 = int(dets[0,0,i,5]*w)
            y2 = int(dets[0,0,i,6]*h)
            bbox_h = y2 - y1
            if bbox_h <= 0:
                return False, None, None
            dist = (FOCAL_LENGTH * KNOWN_HEIGHT) / bbox_h
            cx = (x1 + x2)//2
            return True, dist, cx

    return False, None, None

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: cannot open camera"); return

    try:
        # 1) Spin until we see a person
        print("👉 Spinning to search for person...")
        while True:
            spin(MOTOR_SPEED)
            ret, frame = cap.read()
            if not ret: break

            seen, dist, cx = detect_person(frame)
            if seen:
                stop()
                print(f"✅ Person detected at ~{dist:.2f} m")
                break

        # 2) Drive toward them
        print("🚗 Approaching person...")
        while True:
            ret, frame = cap.read()
            if not ret: break

            seen, dist, cx = detect_person(frame)
            if not seen:
                stop()
                print("⚠️ Lost sight—stopping.")
                break

            if dist <= STOP_DISTANCE:
                stop()
                print("🎯 Reached target distance.")
                break

            # decide turn vs. forward
            if cx < frame.shape[1]*0.4:
                # turn left in arc
                pwm_a.ChangeDutyCycle(MOTOR_SPEED)
                pwm_b.ChangeDutyCycle(MOTOR_SPEED)
                GPIO.output(IN1, GPIO.LOW);  GPIO.output(IN2, GPIO.HIGH)
                GPIO.output(IN3, GPIO.HIGH); GPIO.output(IN4, GPIO.LOW)
                print("← Turning left")
            elif cx > frame.shape[1]*0.6:
                # turn right in arc
                pwm_a.ChangeDutyCycle(MOTOR_SPEED)
                pwm_b.ChangeDutyCycle(MOTOR_SPEED)
                GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
                GPIO.output(IN3, GPIO.LOW);  GPIO.output(IN4, GPIO.HIGH)
                print("→ Turning right")
            else:
                # straight ahead
                pwm_a.ChangeDutyCycle(MOTOR_SPEED)
                pwm_b.ChangeDutyCycle(MOTOR_SPEED)
                GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
                GPIO.output(IN3, GPIO.HIGH); GPIO.output(IN4, GPIO.LOW)
                print("↑ Moving forward")

            cv2.imshow("Tracking", frame)
            if cv2.waitKey(1) == 27:  # ESC to quit
                stop()
                break

    finally:
        print("Cleaning up GPIO & camera...")
        pwm_a.stop(); pwm_b.stop()
        GPIO.cleanup()
        cap.release()
        cv2.destroyAllWindows()

if __name__=="__main__":
    main()
