import cv2
import requests

# URL of the stream
url = "http://192.168.4.1/stream"

# Function to draw multicolored lines
def draw_multicolored_line(image, start, end):
    line_len = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
    segment_len = line_len / 3

    points = [start]
    for i in range(1, 3):
        interp_x = int(start[0] + i * (end[0] - start[0]) / 3)
        interp_y = int(start[1] + i * (end[1] - start[1]) / 3)
        points.append((interp_x, interp_y))
    points.append(end)

    colors = [(0, 0, 255), (0, 255, 255), (0, 255, 0)]
    for i in range(3):
        image = cv2.line(image, points[i], points[i + 1], colors[i], 2)
    return image

# Open the video stream
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Cannot open stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot grab frame")
        break

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Define the guidelines for the backup camera
    top_left = (int(width * 0.3), int(height * 0.5))
    top_right = (int(width * 0.7), int(height * 0.5))
    bottom_left = (int(width * 0.1), height)
    bottom_right = (int(width * 0.9), height)

    # Draw the multicolored vertical guidelines
    frame = draw_multicolored_line(frame, top_left, bottom_left)
    frame = draw_multicolored_line(frame, top_right, bottom_right)

    # Draw the top guideline in green
    frame = cv2.line(frame, top_left, top_right, (0, 0, 255), 2)

    # Display the frame with guidelines
    cv2.imshow('Image with Guidelines', frame)

    # Press 'q' to quit the image display
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()

