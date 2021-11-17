#!/usr/bin/python3

# --------------------------------------------------
# Import Modules
# --------------------------------------------------
import argparse
import numpy as np
# import cv2.cv2 as cv2
import cv2
import json
import os
import sys
from collections import namedtuple
from pprint import pprint
from prettyprinter import cpprint
from time import time, ctime
from colorama import Fore, Back, Style
from numpy.random import randint
from my_classes import *
from my_functions import *
import readchar
from statistics import mean
from prettyprinter import set_default_style
from prettyprinter import install_extras
from termcolor import colored, cprint

install_extras(['python'])
set_default_style('light')


# ---------------------------------------------------
# Script of a Augmented Reality Paint - Assignment 2 - PSR. Example of similar software here:
# https://www.youtube.com/watch?v=ud119RI_Rpg
#
#
# Contributors:
#   - Lucas Rodrigues Dal'Col
#   - Manuel Alberto Silva Gomes
#   - Emanuel Krzysztoń
#   - João Pedro Tira Picos Costa Nunes
#
# PSR, University of Aveiro, November 2021.
# ---------------------------------------------------


def main():
    # ---------------------------------------------------
    # Initialization
    # ---------------------------------------------------

    # Create argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('-j', '--json', required=True, help="Definition of test mode")
    args = vars(ap.parse_args())

    # Opening JSON file
    f = open(args['json'])

    # returns JSON object as a dictionary
    limits = json.load(f)

    # Setting up the video capture
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()

    # Setting up timer
    start_time = tic()

    # Setting up the painting interface. White blank image.
    windowWidth = frame.shape[1]
    windowHeight = frame.shape[0]

    blank_image = 255 * np.ones(shape=[windowHeight, windowWidth, 3], dtype=np.uint8)
    cv2.imshow("White Blank", blank_image)

    # Setting up variables
    toggle = False
    radio = 5
    color = (255, 0, 0)
    color_str = 'BLUE'
    center = (200, 200)
    print('You are painting with color ' + color_str + ' and pencil size ' + str(radio))

    # ---------------------------------------------------
    # Execution
    # ---------------------------------------------------
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        # Create mask
        mask_original = createMask(limits, frame)

        # Find centroid
        mask, centroid = findCentroid(mask_original)

        # Paint the original image green
        frame = greenBlob(frame, mask)

        # Keyboard commands
        choice = cv2.waitKey(1)

        # if a key is pressed
        if choice != -1:

            # Choose the color blue if "b" is pressed.
            if choice == ord('b'):
                color = (255, 0, 0)
                color_str = 'BLUE'
                print(Fore.BLUE + color_str + ' color selected.' + Style.RESET_ALL)

            # Choose the color green if "g" is pressed.
            elif choice == ord('g'):
                color = (0, 255, 0)
                color_str = 'GREEN'
                print(Fore.GREEN + color_str + ' color selected.' + Style.RESET_ALL)
            # Choose the color red if "r" is pressed.
            elif choice == ord('r'):
                color = (0, 0, 255)
                color_str = 'RED'
                print(Fore.RED + color_str + ' color selected.' + Style.RESET_ALL)

            # Increase the pencil size if "+" is pressed.
            elif choice == ord('+'):
                radio = radio + 1
                print('Pencil size is now ' + Fore.GREEN + str(radio) + Style.RESET_ALL)
            # Decrease the pencil size if "-" is pressed.
            elif choice == ord('-'):
                radio = radio - 1
                if radio <0:
                    radio = 0
                print('Pencil size is now ' + Fore.RED + str(radio) + Style.RESET_ALL)

            # Clear the window if "c" is pressed.
            elif choice == ord('c'):
                blank_image = 255 * np.ones(shape=[windowHeight, windowWidth, 3], dtype=np.uint8)
                print('You pressed "c": The window "White Blank" was cleared.')

            # Save the current image if "w" is pressed.
            elif choice == ord('w'):
                date = ctime()
                cv2.imwrite('drawing_' + date + '.png', blank_image)
                print('Current image saved as: ' + Fore.BLUE + 'drawing_' + date + '.png' + Style.RESET_ALL)

        if centroid is None:
            pass
        else:
            # Change the variable centroid to a tuple in center
            center = (int(centroid[0]), int(centroid[1]))
            # Paint a dot according to the inputs
            cv2.circle(blank_image, center, radio, color, -1)

        # Measure the time
        toggle = periodDefinition(start_time, toggle, 5)
        if toggle:
            print('Now showing the real image')


        # Show the webcam frame, the mask and the image being painted
        cv2.imshow("Original", frame)
        cv2.imshow("Mask", mask_original)
        cv2.imshow("White Blank", blank_image)

        # If you press q, the program shuts down
        if choice & 0xFF == ord('q'):
            print(Fore.RED + 'You pressed "q". The program closed.' + Style.RESET_ALL)
            break

    # When everything done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
