import cv2
import numpy as np
import math
import torch

# Screen dimensions (adjust according to your frame size if different)
WIDTH, HEIGHT = 1024, 760

# Colors (BGR format for OpenCV)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)
RED = (0, 0, 255)

# Vehicle properties
top_vehicle_pos = (WIDTH // 2 - 200, (HEIGHT // 2) + 200)
bottom_vehicle_pos = (WIDTH // 2 + 200, (HEIGHT // 2) + 200)
wheel_angle = 0
TURN_ANGLE = 2   # Angle to turn per key press
PATH_LENGTH = 100  # Total number of steps for the path

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Load YOLOv5s model
def draw_vehicle_path(frame, top_pos, bottom_pos, wheel_angle):
    # Draw initial vehicle positions
    cv2.circle(frame, top_pos, 5, RED, -1)
    cv2.circle(frame, bottom_pos, 5, RED, -1)

    # Initialize variables for both paths
    x_top, y_top = top_pos
    x_bot, y_bot = bottom_pos
    angle = 90  # Start with the vehicle pointing upwards (90 degrees)

    for i in range(PATH_LENGTH):
        # Determine the color based on the position in the path
        if i < PATH_LENGTH / 3:
            color = GREEN
        elif i < 2 * PATH_LENGTH / 3:
            color = YELLOW
        else:
            color = RED

        # Update angle based on wheel angle
        angle += wheel_angle * 0.1  # Adjust the curvature

        # Convert angle to radians
        rad = math.radians(angle)

        # Move forward in the direction of the current angle for both paths
        x_top -= int(5 * math.cos(rad))
        y_top -= int(5 * math.sin(rad))
        x_bot -= int(5 * math.cos(rad))
        y_bot -= int(5 * math.sin(rad))

        # Draw the paths with the determined color
        cv2.circle(frame, (x_top, y_top), 3, color, -1)
        cv2.circle(frame, (x_bot, y_bot), 3, color, -1)


def detect_objects(frame, model):
    # Perform object detection
    results = model(frame)

    # Parse results
    detections = results.xyxy[0].cpu().numpy()  # Get detections as numpy array

    for detection in detections:
        x1, y1, x2, y2, conf, cls = detection
        label = model.names[int(cls)]
        if label in ['car', 'person']:
            color = GREEN if label == 'person' else YELLOW
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, f'{label} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def main():
    global wheel_angle

    # Load the existing frame (screenshot)
    # image_path = 'Screenshot 2024-06-06 110337.jpeg'
    url = 'http://192.168.4.1/stream'
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("cannot open capture")
        return

    # frame = cv2.imread(image_path)
    # if frame is None:
    #     print("Error: Image not found or unable to load.")
    #     return

    # Ensure the frame is the correct size (optional)
    # frame = cv2.resize(frame, (WIDTH, HEIGHT))
    
    cv2.namedWindow("Backup Camera HUD")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("error")
            break
        
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        hud_frame = frame.copy()
        draw_vehicle_path(hud_frame, top_vehicle_pos, bottom_vehicle_pos, wheel_angle)
        detect_objects(hud_frame, model)
        cv2.imshow("Backup Camera HUD", hud_frame)

        key = cv2.waitKey(30)
        if key == 27:  # ESC key to exit
            break
        elif key == ord('a'):
            wheel_angle += TURN_ANGLE
        elif key == ord('d'):
            wheel_angle -= TURN_ANGLE
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

