#!/usr/bin/python3

# --------------------------------------------------
# Import Modules
# --------------------------------------------------
import argparse
import copy
import numpy as np
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
import math
from skimage.metrics import structural_similarity as ssim

install_extras(['python'])
set_default_style('light')
draw = False



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

def onMouse(event, x, y, flags, param):
    global isdown
    global center_mouse

    if event == cv2.EVENT_MOUSEMOVE:
        if isdown:
            center_mouse = (x, y)

    if event == cv2.EVENT_LBUTTONDOWN:
        isdown = True
        center_mouse = (x, y)

    if event == cv2.EVENT_LBUTTONUP:
        isdown = False


def main():
    # ---------------------------------------------------
    # Initialization
    # ---------------------------------------------------
    # Starting global variables
    global numeric_paint_blank_image, painted_image, isdown, center_mouse

    # Create argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('-j', '--json', required=True, help="Input json file path")
    ap.add_argument('-usp', '--use_shake_prevention', action='store_true',
                    help='Select this option to use shake prevention.')
    ap.add_argument('-unp', '--use_numeric_paint', action='store_true',
                    help='Select this option to use numeric paint.')
    args = vars(ap.parse_args())

    # Opening JSON file
    with open(args['json']) as file_handle:
        # returns JSON object as a dictionary
        limits = json.load(file_handle)

    # Setting up the video capture
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()

    # Setting up timer
    start_time = tic()

    # Setting up the painting interface. Canvas image.
    window_width = frame.shape[1]
    window_height = frame.shape[0]
    blank_image = 255 * np.ones(shape=[window_height, window_width, 3], dtype=np.uint8)

    cprint('Welcome to our Augmented Reality Paint! ENJOY!'
           , color='white', on_color='on_green', attrs=['blink'])

    print("\n\nContributors: \n- Lucas Rodrigues Dal'Col \n- Manuel Alberto Silva Gomes"
          " \n- Emanuel Krzysztoń \n- João Pedro Tira Picos Costa Nunes \n\nPSR, University of Aveiro, "
          "November 2021.\n")

    if args['use_numeric_paint']:
        cprint('You chose numeric paint mode!'
               , color='white', on_color='on_blue', attrs=['blink'])

        blank_image, painted_image = drawNumericPaintImage(blank_image=blank_image)
        numeric_paint_blank_image = copy.deepcopy(blank_image)

        # print to the user which color should he print in it index
        print('\nColor index 1 corresponds to ' + Fore.BLUE + 'blue ' + Fore.RESET + 'color.')
        print('Color index 2 corresponds to ' + Fore.GREEN + 'green ' + Fore.RESET + 'color.')
        print('Color index 3 corresponds to ' + Fore.RED + 'red ' + Fore.RESET + 'color.')
        print("\nYou can also check the 'Painted image' to see how it should be like")
        print('Press the space bar to finish and evaluate your painting...\n')

        cv2.imshow('Painted image', painted_image)

    cv2.imshow("Canvas", blank_image)
    cv2.setMouseCallback("Canvas", onMouse)

    # Setting up variables
    toggle = False
    isdown = False
    radio = 5
    # global color
    color = (255, 0, 0)
    color_str = 'BLUE'
    center = (200, 200)
    center_mouse = (200, 200)
    center_prev = (200, 200)
    center_prev_mouse = (200, 200)

    if args['use_shake_prevention']:  # if the user uses the shake prevention
        print(Fore.BLUE + Back.WHITE + 'You are using shake prevention.' + Style.RESET_ALL)
        shake_prevention_on = 1
    else:
        shake_prevention_on = 0

    print('You started your paint with color ' + Fore.BLUE + color_str + Fore.RESET + ' and pencil size ' + Fore.GREEN +
          str(radio) + Fore.RESET + ' as default parameters')

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
                print(Fore.BLUE + color_str + ' color selected.        ' + Style.RESET_ALL, end='\r')

            # Choose the color green if "g" is pressed.
            elif choice == ord('g'):
                color = (0, 255, 0)
                color_str = 'GREEN'
                print(Fore.GREEN + color_str + ' color selected.          ' + Style.RESET_ALL, end='\r')
            # Choose the color red if "r" is pressed.
            elif choice == ord('r'):
                color = (0, 0, 255)
                color_str = 'RED'
                print(Fore.RED + color_str + ' color selected.            ' + Style.RESET_ALL, end='\r')

            # Increase the pencil size if "+" is pressed.
            elif choice == ord('+'):
                radio = radio + 1
                print('Pencil size is now ' + Fore.GREEN + str(radio) + Style.RESET_ALL + '      ', end='\r')
            # Decrease the pencil size if "-" is pressed.
            elif choice == ord('-'):
                radio = radio - 1
                if radio < 0:
                    radio = 0
                print('Pencil size is now ' + Fore.RED + str(radio) + Style.RESET_ALL + '      ', end='\r')

            # Clear the window if "c" is pressed.
            elif choice == ord('c'):
                if not args['use_numeric_paint']:
                    blank_image = 255 * np.ones(shape=[window_height, window_width, 3], dtype=np.uint8)
                else:
                    blank_image = numeric_paint_blank_image
                print('\nYou pressed "c": The window "Canvas" was cleared.')

            # Save the current image if "w" is pressed.
            elif choice == ord('w'):
                date = ctime()
                cv2.imwrite('drawing_' + date + '.png', blank_image)
                print('\nCurrent image saved as: ' + Fore.BLUE + 'drawing_' + date + '.png' + Style.RESET_ALL)

        if radio == 0:  # if the thickness of the line is zero the program doesn't draw
            pass
        else:
            if isdown:  # Code for when the user is pressing the mouse
                if shake_prevention_on:  # if the user uses the shake prevention
                    # Calculate the distance between the point of the mouse pressed and the previous point
                    distance_mouse = math.sqrt(((center_mouse[0] - center_prev_mouse[0]) ** 2) + (
                            (center_mouse[1] - center_prev_mouse[1]) ** 2))
                    if distance_mouse > 40:
                        center_prev_mouse = center_mouse  # defining the center_prev to use in the next cycle
                    else:
                        # Paint a line according to the inputs
                        cv2.line(blank_image, center_prev_mouse, center_mouse, color, radio)
                        center_prev_mouse = center_mouse  # defining the center_prev to use in the next cycle
                else:
                    # Paint a line according to the inputs
                    cv2.line(blank_image, center_prev_mouse, center_mouse, color, radio)
                    center_prev_mouse = center_mouse  # defining the center_prev to use in the next cycle
            else:  # Code for when the user is not pressing the mouse
                if centroid is None:
                    pass
                else:
                    # Change the variable centroid to a tuple in center
                    center = (int(centroid[0]), int(centroid[1]))

                    if shake_prevention_on:  # if the user uses the shake prevention

                        # Calculate the distance between the centroid detected and the previous centroid detected
                        distance = math.sqrt(((center[0] - center_prev[0]) ** 2) + ((center[1] - center_prev[1]) ** 2))
                        if distance > 40:  # if the distance is bigger than a defined number, the program doesn't paint
                            center_prev = center  # defining the center_prev to use in the next cycle
                        else:
                            # Paint a line according to the inputs
                            cv2.line(blank_image, center_prev, center, color, radio)
                            center_prev = center  # defining the center_prev to use in the next cycle
                    else:
                        # Paint a line according to the inputs
                        cv2.line(blank_image, center_prev, center, color, radio)
                        center_prev = center  # defining the center_prev to use in the next cycle

        if not args['use_numeric_paint']:
            # Measure the time
            toggle = periodDefinition(start_time, toggle, 5)
            # If we are in the period defined
            if toggle:
                # Replacing the white canvas with the real frame
                blend_image = createBlend(blank_image, frame)
                # Showing the blend image
                cv2.imshow("Canvas", blend_image)
            else:
                # Showing the white canvas
                cv2.imshow("Canvas", blank_image)
        else:
            # Showing the white canvas
            cv2.imshow("Canvas", blank_image)

            # If you press space bar, the program shuts down
            if choice & 0xFF == ord(' '):
                print(Fore.BLUE + '\nYou pressed the space bar. Here it is your statistics:' + Style.RESET_ALL)
                mean_square_error = mse(painted_image, blank_image)
                similarity = ssim(painted_image, blank_image, multichannel=True)

                print('Mean Square Error: ' + str(round(mean_square_error, 2)) + ' , Structural Similarity: '
                      + str(round(similarity * 100, 2)) + ' %')
                if 0 <= similarity < 0.5:
                    cprint('Your painting is not even 50% to the correct one. Keep practicing!'
                            , color='white', on_color='on_red', attrs=['blink'])
                elif 0.5 <= similarity < 0.75:
                    cprint('You were good, but can be better.'
                           , color='white', on_color='on_blue', attrs=['blink'])
                elif 0.75 <= similarity <= 1.0:
                    cprint('AWESOME, your painting is amazing'
                           , color='white', on_color='on_green', attrs=['blink'])

                compareImages(painted_image, blank_image)

                cv2.waitKey(0)

                break

        # Show the webcam frame and the mask
        cv2.imshow("Original", frame)
        cv2.imshow("Mask", mask_original)

        # If you press q, the program shuts down
        if choice & 0xFF == ord('q'):
            print(Fore.RED + '\nYou pressed "q". The program closed.' + Style.RESET_ALL)
            break

    # ---------------------------------------------------
    # Terminating
    # ---------------------------------------------------
    # When everything done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
