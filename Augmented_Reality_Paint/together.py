#!/usr/bin/python3
import cv2
import numpy as np
import math

draw = False
point1 = ()
point2 = ()
ix, iy = -1, -1
radius = 0
choice = cv2.waitKey(1)

def draw_rectangle(event, x, y, flags, params):
    global point1, point2, draw

    if event == cv2.EVENT_LBUTTONDOWN:
        if draw is False:
            draw = True
            point1 = (x, y)
        else:
            draw = False

    elif event == cv2.EVENT_MOUSEMOVE:
        if draw is True:
            point2 = (x, y)


# Create a function based on a CV2 Event (Left button click)
def draw_circle(event, x, y, flags, param):
    global ix, iy, draw, radius

    if event == cv2.EVENT_LBUTTONDOWN:
        draw = True
        # we take note of where that mouse was located
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        draw == True

    elif event == cv2.EVENT_LBUTTONUP:
        radius = int(math.sqrt(((ix - x) ** 2) + ((iy - y) ** 2)))
        cv2.circle(capture, (ix, iy), radius, (0, 0, 255), thickness=1)
        draw = False

capture = cv2.VideoCapture(0)

cv2.namedWindow("Frame")

while True:
    ret, frame = capture.read()
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord('s'):
        cv2.setMouseCallback("Frame", draw_rectangle)
        if point1 and point2:
            cv2.rectangle(frame, point1, point2, (0, 255, 0))
    elif key == ord('o'):
        cv2.setMouseCallback('Frame', draw_circle)
        if ix and iy:
            cv2.circle(frame, (ix, iy), radius, (0, 0, 255), 1)

    cv2.imshow("Frame", frame)

capture.release()
cv2.destroyAllWindows()
