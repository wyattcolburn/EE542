import cv2
import numpy as np
import math

# Screen dimensions (adjust according to your frame size if different)
WIDTH, HEIGHT = 800, 600

# Colors (BGR format for OpenCV)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)
RED = (0, 0, 255)

# Vehicle properties
top_vehicle_pos = (WIDTH // 2 - 100, (HEIGHT // 2) - 100)
bottom_vehicle_pos = (WIDTH // 2 + 100, (HEIGHT // 2) - 100)
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
    angle_top = 90  # Start with the vehicle pointing upwards (90 degrees)
    angle_bot = 90

    for i in range(PATH_LENGTH):
        # Determine the color based on the position in the path
        if i < PATH_LENGTH / 3:
            color = RED
        elif i < 2 * PATH_LENGTH / 3:
            color = YELLOW
        else:
            color = GREEN

        # Update angle based on wheel angle
        angle_change = wheel_angle * 0.1  # Adjust the curvature
        angle_top += angle_change
        angle_bot += angle_change

        # Convert angle to radians
        rad_top = math.radians(angle_top)
        rad_bot = math.radians(angle_bot)

        # Move forward in the direction of the current angle for both paths
        x_top += int(5 * math.cos(rad_top))
        y_top += int(5 * math.sin(rad_top))
        x_bot += int(5 * math.cos(rad_bot))
        y_bot += int(5 * math.sin(rad_bot))

        # Adjust path length to simulate inner and outer curves
        if wheel_angle != 0:
            path_ratio = 1.0 + (abs(wheel_angle) / 20.0)
            if wheel_angle > 0:  # Turning right
                y_bot += int(5 * path_ratio * math.sin(rad_bot))
            else:  # Turning left
                y_top += int(5 * path_ratio * math.sin(rad_top))

        # Draw the paths with the determined color
        cv2.circle(frame, (x_top, y_top), 3, color, -1)
        cv2.circle(frame, (x_bot, y_bot), 3, color, -1)

def main():
    global wheel_angle

    # Load the existing frame (screenshot)
    image_path = 'Screenshot 2024-06-06 110337.jpeg'
    frame = cv2.imread(image_path)
    if frame is None:
        print("Error: Image not found or unable to load.")
        return

    # Ensure the frame is the correct size (optional)
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    
    cv2.namedWindow("Backup Camera HUD")

    while True:
        hud_frame = frame.copy()
        draw_vehicle_path(hud_frame, top_vehicle_pos, bottom_vehicle_pos, wheel_angle)
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


