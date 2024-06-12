import cv2
import torch
import numpy as np
from pathlib import Path

# URL of the MJPEG stream
url = "http://192.168.4.1/stream"

# Use OpenCV to capture the MJPEG stream
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Cannot open stream")
    exit()

# Load YOLOv5 model from local weights file
weights_path = 'yolov5s.pt'  # Update this path if needed
if not Path(weights_path).is_file():
    print(f"Cannot find the YOLOv5 weights file at {weights_path}")
    exit()

# Load the model
model = torch.hub.load('ultralytics/yolov5', 'pretrained', path_or_model=weights_path)

# Set the model to evaluation mode
model.eval()

# Predefined colors for the bounding boxes
colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in range(model.yaml['nc'])]

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Define the guidelines for the backup camera
    top_left = (int(width * 0.3), int(height * 0.5))
    top_right = (int(width * 0.7), int(height * 0.5))
    bottom_left = (int(width * 0.1), height)
    bottom_right = (int(width * 0.9), height)

    # Draw the guidelines
    frame = cv2.line(frame, top_left, bottom_left, (0, 255, 0), 2)
    frame = cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
    frame = cv2.line(frame, top_left, bottom_left, (0, 255, 0), 2)
    frame = cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
    frame = cv2.line(frame, top_left, bottom_left, (0, 255, 0), 2)
    frame = cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
    frame = cv2.line(frame, top_left, top_right, (0, 255, 0), 2)

    # Preprocess the frame for YOLOv5
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (640, 640))  # Resize to 640x640
    img = img.astype(np.float32) / 255.0  # Normalize to [0, 1]
    img = np.transpose(img, (2, 0, 1))  # HWC to CHW
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    img = torch.from_numpy(img)  # Convert to torch tensor

    # Run YOLOv5 inference on the frame
    with torch.no_grad():
        results = model(img)

    # Process detections
    for *box, conf, cls in results.xyxy[0]:  # x1, y1, x2, y2, conf, cls
        label = f"{model.names[int(cls)]} {conf:.2f}"
        color = colors[int(cls)]
        x1, y1, x2, y2 = map(int, box)
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        frame = cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display the frame
    cv2.imshow('ESP32 Stream', frame)
    
    # Press 'q' to quit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

