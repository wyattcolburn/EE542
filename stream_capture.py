import cv2
import requests

url = "http://192.168.4.1/stream"  

# Use OpenCV to capture the MJPEG stream
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Cannot open stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
       # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Define the guidelines for the backup camera
    # You can adjust these coordinates to fit your specific needs
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

    cv2.imshow('ESP32 Stream', frame)
    
    # Press 'q' to quit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

