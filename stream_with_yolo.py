import cv2
import torch
from pathlib import Path
from models.common import DetectMultiBackend
from utils.general import non_max_suppression, scale_boxes
from utils.torch_utils import select_device

# Initialize YOLOv5 model
weights = 'yolov5s.pt'
device = select_device('')
model = DetectMultiBackend(weights, device=device, dnn=False)
stride, names, pt = model.stride, model.names, model.pt
imgsz = (640, 640)
half = device.type != 'cpu'  # half precision only supported on CUDA

# Load the model
model.warmup(imgsz=(1 if pt else 1, 3, *imgsz))  # warmup
if half:
    model.model.half()  # to FP16

# Initialize video stream
url = "http://192.168.4.1/stream"
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Cannot open stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Pre-process the frame
    img = cv2.resize(frame, imgsz)  # resize
    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255  # 0 - 255 to 0.0 - 1.0
    if len(img.shape) == 3:
        img = img[None]  # expand for batch dim

    # Run inference
    pred = model(img, augment=False, visualize=False)
    pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)

    # Process detections
    for i, det in enumerate(pred):  # per image
        if len(det):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], frame.shape).round()
            for *xyxy, conf, cls in reversed(det):
                label = f'{names[int(cls)]} {conf:.2f}'
                cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Draw guidelines for the backup camera
    height, width, _ = frame.shape
    top_left = (int(width * 0.3), int(height * 0.5))
    top_right = (int(width * 0.7), int(height * 0.5))
    bottom_left = (int(width * 0.1), height)
    bottom_right = (int(width * 0.9), height)

    frame = cv2.line(frame, top_left, bottom_left, (0, 255, 0), 2)
    frame = cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
    frame = cv2.line(frame, top_left, top_right, (0, 255, 0), 2)

    # Display the frame with detections
    cv2.imshow('ESP32 Stream', frame)
    
    # Press 'q' to quit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

