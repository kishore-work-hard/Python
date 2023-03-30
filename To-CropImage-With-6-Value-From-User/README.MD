This is a Python script that allows the user to select a polygonal region of interest (ROI) in an image and crops it. The script uses the OpenCV library for image processing and the JSON library for storing the ROI points.

The script first checks if a JSON file called "six_points.json" exists. If it does, it reads the ROI points from the file. If not, it initializes an empty list for the points.

The crop function takes in the list of points and uses them to draw a green box around the selected ROI on the input image. It then creates a black image with the same dimensions as the input image and creates a mask by filling a polygon with the ROI points. The mask is then applied to the input image to obtain a masked image of the selected ROI. The masked region is then pasted onto the black image. The resulting black image with the masked region is displayed.

The draw_box function is a callback function for mouse events. When the left button is clicked, it appends the (x, y) coordinates of the click to the points list. If there are 6 points in the list (i.e. a polygon with 6 vertices has been selected), it calls the crop function and saves the points to the JSON file.

If the points list has 6 points, the crop function is called and the ROI is cropped. Otherwise, a window is created to display the input image. The draw_box function is set as the mouse callback function for the window. The image is displayed and the script waits for a key press. Once a key is pressed, the window is closed and the script exits.
