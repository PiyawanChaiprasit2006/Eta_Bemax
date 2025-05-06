# import libraries
import numpy as np
import cv2

# path to the prototxt file and the caffemodel
prototxt = "MobileNetSSD_deploy.prototxt"
caffe_model = "MobileNetSSD_deploy.caffemodel"

# load the model
net = cv2.dnn.readNetFromCaffe(prototxt, caffe_model)

# class labels
classNames = {
    0: 'background', 1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
    14: 'motorbike', 15: 'person', 16: 'pottedplant',
    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'
}

# known real-world object heights (in meters)
KNOWN_HEIGHTS = {
    "person": 1.7,
    "bottle": 0.25,
    "chair": 0.8,
    "car": 1.5
}

# estimated focal length in pixels (adjust this after calibration)
FOCAL_LENGTH = 615

# start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]

    # preprocess image
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1/127.5, size=(300, 300),
                                 mean=(127.5, 127.5, 127.5), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()

    # process detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            class_id = int(detections[0, 0, i, 1])
            if class_id in classNames:
                label_name = classNames[class_id]

                x1 = int(detections[0, 0, i, 3] * width)
                y1 = int(detections[0, 0, i, 4] * height)
                x2 = int(detections[0, 0, i, 5] * width)
                y2 = int(detections[0, 0, i, 6] * height)
                bbox_height = y2 - y1

                # draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # estimate distance
                if label_name in KNOWN_HEIGHTS and bbox_height > 0:
                    real_height = KNOWN_HEIGHTS[label_name]
                    distance = (FOCAL_LENGTH * real_height) / bbox_height
                    distance_text = f"{distance:.2f} m"

                    # show distance above box
                    cv2.putText(frame, distance_text, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                # show class name and confidence
                label = f"{label_name}: {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # display the result
    cv2.imshow("Object Detection with Distance", frame)
    if cv2.waitKey(1) == 27:  # Press ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
