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

# ---------------------------------------------------
# Global Variables
# ---------------------------------------------------
min_B = 0
max_B = 255
min_G = 0
max_G = 255
min_R = 0
max_R = 255

# ----------------------------------------------------
# Function Definition
# ----------------------------------------------------
# Define functions of trackbars
def minOnTrackbarBChannel(threshold):
    """
    Trackbar for the minimum threshold for the Blue (RGB) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global min_B
    min_B = threshold


def maxOnTrackbarBChannel(threshold):
    """
    Trackbar for the maximum threshold for the Blue (RGB) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global max_B
    max_B = threshold


def minOnTrackbarGChannel(threshold):
    """
    Trackbar for the minimum threshold for the Green (RGB) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global min_G
    min_G = threshold


def maxOnTrackbarGChannel(threshold):
    """
    Trackbar for the maximum threshold for the Green (RGB) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global max_G
    max_G = threshold


def minOnTrackbarRChannel(threshold):
    """
    Trackbar for the minimum threshold for the Red (RGB) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global min_R
    min_R = threshold


def maxOnTrackbarRChannel(threshold):
    """
    Trackbar for the maximum threshold for the Red (RGB) channel
    :param threshold: the threshold for the channel in question. Datatype: int
    """
    global max_R
    max_R = threshold


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

    # Create trackbars to control the threshold of the binarization
    cv2.createTrackbar('min B', window_name_2, 0, 255, minOnTrackbarBChannel)
    cv2.createTrackbar('max B', window_name_2, 0, 255, maxOnTrackbarBChannel)
    cv2.createTrackbar('min G', window_name_2, 0, 255, minOnTrackbarGChannel)
    cv2.createTrackbar('max G', window_name_2, 0, 255, maxOnTrackbarGChannel)
    cv2.createTrackbar('min R', window_name_2, 0, 255, minOnTrackbarRChannel)
    cv2.createTrackbar('max R', window_name_2, 0, 255, maxOnTrackbarRChannel)

    # Set the trackbar position to 255 for maximum trackbars
    cv2.setTrackbarPos('max B', window_name_2, 255)
    cv2.setTrackbarPos('max G', window_name_2, 255)
    cv2.setTrackbarPos('max R', window_name_2, 255)

    # Prints to make the program user friendly, present to the user the hotkeys
    print(Back.GREEN + 'Start capturing the webcam video.' + Back.RESET)
    print(Fore.GREEN + 'press w to exit and save the threshold limits' + Fore.RESET)
    print(Fore.RED + 'press q to exit without saving the threshold limits' + Fore.RESET)

    # ---------------------------------------------------
    # Execution
    # ---------------------------------------------------
    # While cycle to update the values of the trackbar at the time and show video from webcam
    while True:
        # Get an image from the camera (a frame) and show
        _, frame = capture.read()
        cv2.imshow(window_name_1, frame)

        # Get ranges for each channel from trackbar
        limits = {'B': {'min': min_B, 'max': max_B},
                  'G': {'min': min_G, 'max': max_G},
                  'R': {'min': min_R, 'max': max_R}}

        # Convert the dict structure created before to numpy arrays, because is the structure that opencv uses it.
        mins = np.array([limits['B']['min'], limits['G']['min'], limits['R']['min']])
        maxs = np.array([limits['B']['max'], limits['G']['max'], limits['R']['max']])

        # Create mask using cv2.inRange. The output is still in uint8
        segmented = cv2.inRange(frame, mins, maxs)

        # Show segmented image
        cv2.imshow(window_name_2, segmented)  # Display the image

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
                json.dump(limits, file_handle)  # ranges is the dictionary

            break

    # ---------------------------------------------------
    # Terminating
    # ---------------------------------------------------
    # Release and close everything if it is all finished
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
