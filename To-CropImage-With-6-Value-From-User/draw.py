import json
import cv2
import numpy as np
import json
import os

# Check if the JSON file exists
if os.path.isfile("six_points.json"):
    # Read the points from the JSON file
    with open("six_points.json", "r") as f:
        points = json.load(f)
else:
    # Define an empty list for the points
    points = []

def crop(points):
    # Draw the box
    cv2.line(img, points[0], points[1], (0, 255, 0), 2)
    cv2.line(img, points[1], points[2], (0, 255, 0), 2)
    cv2.line(img, points[2], points[3], (0, 255, 0), 2)
    cv2.line(img, points[3], points[4], (0, 255, 0), 2)
    cv2.line(img, points[4], points[5], (0, 255, 0), 2)
    cv2.line(img, points[5], points[0], (0, 255, 0), 2)

    # Create a black image with the same dimensions as the input image
    black_img = np.zeros_like(img)

    # Create a mask by drawing a filled polygon using the points
    mask = np.zeros(img.shape[:2], np.uint8)
    pts = np.array(points, np.int32)
    cv2.fillPoly(mask, [pts], (255, 255, 255))

    # Apply the mask to the input image
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    # Paste the masked region onto the black image
    mask_color = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    black_img[np.where((mask_color == (255, 255, 255)).all(axis=2))] = masked_img[
        np.where((mask_color == (255, 255, 255)).all(axis=2))]

    # Display the black image with the masked region
    cv2.imshow("Masked Image", black_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Define the callback function for mouse events
def draw_box(event, x, y, flags, params):
    global points, img
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        if len(points) == 6:
            crop(points)
            # Save the points to the JSON file
            with open("six_points.json", "w") as f:
                json.dump(points, f)


# Open the image
img = cv2.imread("image.jpg")

# Check if points have already been marked
if len(points) == 6:
    crop(points)

else:
    # Initialize the list of points
    points = []

    # Create a window to display the image
    cv2.namedWindow("Image")

    # Set the mouse callback function for the window
    cv2.setMouseCallback("Image", draw_box)

    # Display the image
    cv2.imshow("Image", img)

    # Wait for a key press
    cv2.waitKey(0)

    # Clean up
    cv2.destroyAllWindows()
