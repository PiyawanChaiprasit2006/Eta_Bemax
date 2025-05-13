import numpy as np
import cv2


# Path to the prototxt file and the caffemodel (Linux-style paths)
prototxt = "Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.prototxt"
caffe_model = "Final_Engineering_Project/camera_recognition/MobileNetSSD_deploy.caffemodel"


# Load the model
net = cv2.dnn.readNetFromCaffe(prototxt, caffe_model)

# Class labels
classNames = {
    0: 'background', 1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
    14: 'motorbike', 15: 'person', 16: 'pottedplant',
    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'
}


# Known real-world object heights (in meters)
KNOWN_HEIGHTS = {
    "person": 1.7,
    "bottle": 0.25,
    "chair": 0.8,
    "car": 1.5
}


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


        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])
                if class_id in classNames:
                    label_name = classNames[class_id]
                    x1, y1 = int(detections[0, 0, i, 3] * width), int(detections[0, 0, i, 4] * height)
                    x2, y2 = int(detections[0, 0, i, 5] * width), int(detections[0, 0, i, 6] * height)


                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)


                    # Estimate distance
                    bbox_height = y2 - y1
                    if label_name in KNOWN_HEIGHTS and bbox_height > 0:
                        distance = (FOCAL_LENGTH * KNOWN_HEIGHTS[label_name]) / bbox_height
                        cv2.putText(frame, f"{distance:.2f} m", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)


                    # Show class name and confidence
                    label = f"{label_name}: {confidence:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


        cv2.imshow("Object Detection with Distance", frame)
        if cv2.waitKey(1) == 27:  # Press ESC to quit
            break
finally:
    cap.release()
    cv2.destroyAllWindows()





