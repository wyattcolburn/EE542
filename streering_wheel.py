import cv2
import requests

url = "http://192.168.4.1/stream"

# Use OpenCV to capture the MJPEG stream
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Cannot open stream")
    exit()

# Initial steering angle
steering_angle = 0

# Function to update the guidelines based on the steering angle
def update_guidelines(width, height, angle):
    # Adjust the angle to fit the guidelines' positions
    angle_rad = angle * (3.14159 / 180)
    offset_x = int(width * 0.2 * angle_rad)
    
    top_left = (int(width * 0.3) + offset_x, int(height * 0.5))
    top_right = (int(width * 0.7) + offset_x, int(height * 0.5))
    bottom_left = (int(width * 0.1) + offset_x, height)
    bottom_right = (int(width * 0.9) + offset_x, height)
    
    return top_left, top_right, bottom_left, bottom_right

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Get the dimensions of the frame
    height, width, _ = frame.shape
    
    # Update the guidelines based on the current steering angle
    top_left, top_right, bottom_left, bottom_right = update_guidelines(width, height, steering_angle)
    
    # Draw the guidelines
    frame = cv2.line(frame, top_left, bottom_left, (0, 255, 0), 2)
    frame = cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
    frame = cv2.line(frame, top_left, top_right, (0, 255, 0), 2)
    
    cv2.imshow('ESP32 Stream', frame)
    
    # Press 'q' to quit the video stream
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('a'):
        steering_angle -= 5  # Turn left
    elif key == ord('d'):
        steering_angle += 5  # Turn right

cap.release()
cv2.destroyAllWindows()

