#!/usr/bin/python3

import numpy as np
import cv2
import math

drawing = False  # true if mouse is pressed
ix, iy = -1, -1
radius = 0

# Create a function based on a CV2 Event (Left button click)
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, radius
    # Keyboard commands
    choice = cv2.waitKey(1)

    if choice != -1:
        if choice == ord('c'):
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                # we take note of where that mouse was located
                ix, iy = x, y

            elif event == cv2.EVENT_MOUSEMOVE:
                drawing == True

            elif event == cv2.EVENT_LBUTTONUP:
                radius = int(math.sqrt(((ix - x) ** 2) + ((iy - y) ** 2)))
                cv2.circle(capture, (ix, iy), radius, (0, 0, 255), thickness=1)
                drawing = False


# Create a black image
capture = cv2.VideoCapture(0)

# This names the window so we can reference it
cv2.namedWindow('Frame')

# Connects the mouse button to our callback function
cv2.setMouseCallback('Frame', draw_circle)

while (1):
    _, frame = capture.read()

    if ix and iy:
        cv2.circle(frame,(ix,iy), radius , (0,0,255),1)

    cv2.imshow("Frame", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()
