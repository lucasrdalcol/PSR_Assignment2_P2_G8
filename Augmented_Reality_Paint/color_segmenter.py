#!/usr/bin/python3

# ---------------------------------------------------
# Import Modules
# ---------------------------------------------------
import argparse
import json
import cv2
import numpy as np
from functools import partial
from colorama import Fore, Back, Style
from my_functions import *


# ---------------------------------------------------
# Script of a Augmented Reality Paint - Assignment 2 - PSR. Example of similar software here:
# https://www.youtube.com/watch?v=ud119RI_Rpg
#
#
# Contributors:
#   - Lucas Rodrigues Dal'Col
#   - Manuel Alberto Silva Gomes
#   - Emanuel Krzyszton
#   - João Pedro Tira Picos Costa Nunes
#
# PSR, University of Aveiro, November 2021.
# ---------------------------------------------------


# ----------------------------------------------------
# Function Definition
# ----------------------------------------------------
def onTrackBars(_, window_name):
    """
    Function that is called continuously to get the position of the 6 trackbars created for binarizing an image.
    The function returns these positions in a dictionary and in Numpy Arrays.
    :param _: Obligatory variable from OpenCV trackbars but assigned as a silent variable because will not be used.
    :param window_name: The name of the OpenCV window from where we need to get the values of the trackbars.
    Datatype: OpenCV object
    :return: The dictionary with the limits assigned in the trackbars. Convert the dictionary to numpy arrays because
    of OpenCV and return also.
    'limits' Datatype: Dict
    'mins' Datatype: Numpy Array object
    'maxs' Datatype: Numpy Array object
    """
    # Get ranges for each channel from trackbar and assign to a dictionary
    min_b = cv2.getTrackbarPos('min B', window_name)
    max_b = cv2.getTrackbarPos('max B', window_name)
    min_g = cv2.getTrackbarPos('min G', window_name)
    max_g = cv2.getTrackbarPos('max G', window_name)
    min_r = cv2.getTrackbarPos('min R', window_name)
    max_r = cv2.getTrackbarPos('max R', window_name)

    limits = {'B': {'min': min_b, 'max': max_b},
              'G': {'min': min_g, 'max': max_g},
              'R': {'min': min_r, 'max': max_r}}

    # Convert the dict structure created before to numpy arrays, because is the structure that opencv uses it.
    mins = np.array([limits['B']['min'], limits['G']['min'], limits['R']['min']])
    maxs = np.array([limits['B']['max'], limits['G']['max'], limits['R']['max']])

    return limits, mins, maxs


def main():
    # ---------------------------------------------------
    # Initialization
    # ---------------------------------------------------
    # Get the webcam video capture
    capture = cv2.VideoCapture(0)  # Selecting the camera 0

    # Create windows
    window_name_1 = 'Webcam'
    cv2.namedWindow(window_name_1, cv2.WINDOW_NORMAL)
    window_name_2 = 'Segmented image'
    cv2.namedWindow(window_name_2, cv2.WINDOW_NORMAL)

    # Use partial function for the trackbars
    onTrackBars_partial = partial(onTrackBars, window_name=window_name_2)

    # Create trackbars to control the threshold of the binarization
    cv2.createTrackbar('min B', window_name_2, 0, 255, onTrackBars_partial)
    cv2.createTrackbar('max B', window_name_2, 0, 255, onTrackBars_partial)
    cv2.createTrackbar('min G', window_name_2, 0, 255, onTrackBars_partial)
    cv2.createTrackbar('max G', window_name_2, 0, 255, onTrackBars_partial)
    cv2.createTrackbar('min R', window_name_2, 0, 255, onTrackBars_partial)
    cv2.createTrackbar('max R', window_name_2, 0, 255, onTrackBars_partial)

    # Set the trackbar position to 255 for maximum trackbars
    cv2.setTrackbarPos('max B', window_name_2, 255)
    cv2.setTrackbarPos('max G', window_name_2, 255)
    cv2.setTrackbarPos('max R', window_name_2, 255)

    # Prints to make the program user friendly. Present to the user the hotkeys
    if capture.isOpened() is True:
        print(Back.GREEN + 'Start capturing the webcam video.' + Back.RESET)
        print(Fore.GREEN + 'press w to exit and save the threshold limits' + Fore.RESET)
        print(Fore.RED + 'press q to exit without saving the threshold limits' + Fore.RESET)
    else:
        print(Back.RED + "WARNING!!!" + Back.RESET + Fore.RED + " Can't access the camera" + Fore.RESET)

    # ---------------------------------------------------
    # Execution
    # ---------------------------------------------------
    # While cycle to update the thresholds values from the trackbar to the frame at the time and show video from webcam
    while capture.isOpened():
        # Get an image from the camera (a frame) and show
        _, frame = capture.read()
        cv2.imshow(window_name_1, frame)

        # Get ranges from trackbars in dict and numpy data structures
        limits, mins, maxs = onTrackBars_partial(0)

        # Create mask using cv2.inRange. The output is still in uint8
        segmented_frame = cv2.inRange(frame, mins, maxs)

        # Show segmented image
        cv2.imshow(window_name_2, segmented_frame)  # Display the image

        key = cv2.waitKey(1)  # Wait a key to stop the program

        # Keyboard inputs to finish the cycle
        if key == ord('q'):
            print(Fore.RED + 'Letter q (quit) pressed, exiting the program without saving limits' + Fore.RESET)
            break
        elif key == ord('w'):
            print(Fore.GREEN + 'Letter w (write) pressed, exiting the program and saving limits' + Fore.RESET)
            file_name = 'limits.json'
            with open(file_name, 'w') as file_handle:
                print("writing dictionary with threshold limits to file " + file_name)
                json.dump(limits, file_handle)  # 'limits' is the dictionary

            break

    # ---------------------------------------------------
    # Terminating
    # ---------------------------------------------------
    # Release and close everything if it is all finished
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
