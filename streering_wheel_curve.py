import cv2
import numpy as np
import math

# Screen dimensions (adjust according to your frame size if different)

WIDTH, HEIGHT = 1024, 760

# Colors (BGR format for OpenCV)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)
RED = (0, 0, 255)

# Vehicle properties
top_vehicle_pos = (WIDTH // 2 - 200, (HEIGHT // 2)+ 200)
bottom_vehicle_pos = (WIDTH // 2 + 200, (HEIGHT // 2) + 200)
wheel_angle = 0  # Angle in degrees, 0 means straight
TURN_ANGLE = 2   # Angle to turn per key press
PATH_LENGTH = 100  # Total number of steps for the path

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
            color = RED
        elif i < 2 * PATH_LENGTH / 3:
            color = YELLOW
        else:
            color = GREEN

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
def main():
    global wheel_angle

    # Capture the video stream from the URL
    url = 'http://192.168.4.1/stream'
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("Error: Unable to open video stream.")
        return

    cv2.namedWindow("Backup Camera HUD")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame from video stream.")
            break

        # Ensure the frame is the correct size (optional)
        #frame = cv2.resize(frame, (WIDTH, HEIGHT))

        # Draw the HUD on the frame
        draw_vehicle_path(frame, top_vehicle_pos, bottom_vehicle_pos, wheel_angle)
        cv2.imshow("Backup Camera HUD", frame)

        key = cv2.waitKey(30)
        if key == 27:  # ESC key to exit
            break
        elif key == ord('a'):
            wheel_angle += TURN_ANGLE
        elif key == ord('d'):
            wheel_angle -= TURN_ANGLE
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

