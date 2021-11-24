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
from functools import partial

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

# Callback of mouse
def onMouse(event, x, y, flags, param):
    """
    Retrieving mouse coordinates while left button is clicked
    :param event:
    :param x:
    :param y:
    :param flags:
    :param param:
    :return:
    """
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
        center_mouse = None



def main():
    # ---------------------------------------------------
    # Initialization
    # ---------------------------------------------------
    # Starting global variables
    global numeric_paint_blank_original, painted_image, isdown, center_mouse

    # Setting up variables
    real_toggle = False
    isdown = False
    mouse_painting = True
    radio = 5
    color = (255, 0, 0)
    color_str = 'BLUE'
    center_mouse = (200, 200)
    center_prev = (200, 200)
    center_prev_mouse = (200, 200)
    threshold = 100
    listkeys = []
    listmouse = []

    # Initial print
    cprint('Welcome to our Augmented Reality Paint! ENJOY!'
           , color='white', on_color='on_green', attrs=['blink'])

    print("\n\nContributors: \n- Lucas Rodrigues Dal'Col \n- Manuel Alberto Silva Gomes"
          " \n- Emanuel Krzysztoń \n- João Pedro Tira Picos Costa Nunes \n\nPSR, University of Aveiro, "
          "November 2021.\n")

    # Create argparse
    ap = argparse.ArgumentParser(description='Program to paint on Augmented Reality')
    ap.add_argument('-j', '--json', required=True, help="Input json file path")
    ap.add_argument('-usp', '--use_shake_prevention', action='store_true',
                    help='Select this option to use shake prevention.')
    ap.add_argument('-unp', '--use_numeric_paint', action='store_true',
                    help='Select this option to use numeric paint.')
    args = vars(ap.parse_args())

    # Defining shake prevention
    if args['use_shake_prevention']:  # if the user uses the shake prevention
        print(Fore.BLUE + Back.WHITE + 'You are using shake prevention.' + Style.RESET_ALL)
        shake_prevention_on = 1
    else:
        shake_prevention_on = 0

    # Opening JSON file
    with open(args['json']) as file_handle:
        # returns JSON object as a dictionary
        limits = json.load(file_handle)

    # Setting up the video capture
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()

    # Setting up the painting interface. Canvas image.
    window_width = frame.shape[1]
    window_height = frame.shape[0]
    blank_image = 255 * np.ones(shape=[window_height, window_width, 3], dtype=np.uint8)

    # Setup for numeric paint
    if args['use_numeric_paint']:
        # Print
        cprint('You chose numeric paint mode!'
               , color='white', on_color='on_blue', attrs=['blink'])

        # Generating the numeric picture
        blank_image, painted_image = drawNumericPaintImage(blank_image=blank_image)
        numeric_paint_blank_original = copy.deepcopy(blank_image)

        # Print to the user which color should he print in it index
        print('\nColor index 1 corresponds to ' + Fore.BLUE + 'blue ' + Fore.RESET + 'color.')
        print('Color index 2 corresponds to ' + Fore.GREEN + 'green ' + Fore.RESET + 'color.')
        print('Color index 3 corresponds to ' + Fore.RED + 'red ' + Fore.RESET + 'color.')
        print("\nYou can also check the 'Painted image' to see how it should be like")
        print('Press the space bar to finish and evaluate your painting...\n')

        # Defining the window and showing the painted image
        cv2.namedWindow('Painted Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Painted Image', painted_image)

    # Defining cv2 windows
    cv2.namedWindow('Canvas', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Mask', cv2.WINDOW_NORMAL)

    # Showing the canvas
    cv2.imshow("Canvas", blank_image)

    # Defining mouse callback
    cv2.setMouseCallback("Canvas", onMouse)

    # Print
    print('You started your paint with color ' + Fore.BLUE + color_str + Fore.RESET + ' and pencil size ' + Fore.GREEN +
          str(radio) + Fore.RESET + ' as default parameters. \nYou started painting with the mouse. \nPress ' + Fore.RED + '"n"' + Style.RESET_ALL + ' to paint with the mask. \nPress ' + Fore.RED + '"m"' + Style.RESET_ALL + ' to paint with the mouse again.\nPress ' + Fore.RED + '"v"' + Style.RESET_ALL + ' to toggle between the white canvas and the real frame.')

    # ---------------------------------------------------
    # Execution
    # ---------------------------------------------------
    while video_capture.isOpened():
        # Capture the current frame
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        # Create mask
        mask_original = createMask(limits, frame)

        # Find centroid
        mask, centroid = findCentroid(mask_original)

        # Paint the original image green
        frame = greenBlob(frame, mask)

        # Keyboard commands
        key = cv2.waitKey(1)

        # Append key to list
        listkeys.append(key)

        # Append mouse position to list
        listmouse.append(center_mouse)

        # if a key is pressed
        if key != -1:

            # Choose the color blue if "b" is pressed.
            if key == ord('b'):
                color = (255, 0, 0)
                color_str = 'BLUE'
                print(Fore.BLUE + color_str + ' color selected.                                   ' + Style.RESET_ALL,
                      end='\r')

            # Choose the color green if "g" is pressed.
            elif key == ord('g'):
                color = (0, 255, 0)
                color_str = 'GREEN'
                print(Fore.GREEN + color_str + ' color selected.                                ' + Style.RESET_ALL,
                      end='\r')

            # Choose the color red if "r" is pressed.
            elif key == ord('r'):
                color = (0, 0, 255)
                color_str = 'RED'
                print(Fore.RED + color_str + ' color selected.                                      ' + Style.RESET_ALL,
                      end='\r')

            # Increase the pencil size if "+" is pressed.
            elif key == ord('+'):
                radio = radio + 1
                print('Pencil size is now ' + Fore.GREEN + str(
                    radio) + Style.RESET_ALL + '                               ', end='\r')

            # Decrease the pencil size if "-" is pressed.
            elif key == ord('-'):
                radio = radio - 1
                if radio < 0:
                    radio = 0
                print(
                    'Pencil size is now ' + Fore.RED + str(radio) + Style.RESET_ALL + '                              ',
                    end='\r')

            # Paint with the mouse if "m" is pressed.
            elif key == ord('m'):
                mouse_painting = True
                print('You pressed "m". You are painting with the mouse.             ', end='\r')

            # Paint with the mask if "n" is pressed.
            elif key == ord('n'):
                mouse_painting = False
                print('You pressed "n". You are painting with the mask.                ', end='\r')

            # Toggle a variable to show the real image if "v" is pressed.
            elif key == ord('v'):
                real_toggle = not real_toggle
                if real_toggle:
                    print('You pressed "v". You are seeing the real frame.                ', end='\r')
                else:
                    print('You pressed "v". You are seeing the white canvas.               ', end='\r')

            # Clear the window if "c" is pressed.
            elif key == ord('c'):
                if not args['use_numeric_paint']:
                    blank_image = 255 * np.ones(shape=[window_height, window_width, 3], dtype=np.uint8)
                else:
                    numeric_paint_cleared = copy.deepcopy(numeric_paint_blank_original)
                    blank_image = numeric_paint_cleared
                print('\nYou pressed "c": The window "Canvas" was cleared.')

            # Save the current image if "w" is pressed.
            elif key == ord('w'):
                date = ctime()
                cv2.imwrite('drawing_' + date + '.png', blank_image)
                print('\nCurrent image saved as: ' + Fore.BLUE + 'drawing_' + date + '.png' + Style.RESET_ALL)

            # Draw a rectangle when pressing 's' key
            if key == ord('s'):
                # If it's not on numeric print and it's on "mask" mode
                if not args['use_numeric_paint'] and not mouse_painting:
                    # If the previous pressed key was not s, create a cache and save the starting point
                    if listkeys[-2] != ord('s'):
                        cache = copy.deepcopy(blank_image)
                        start_point = (round(centroid[0]), round(centroid[1]))

                    # If the previous pressed key was an s, draw rectangle
                    else:
                        end_point = (round(centroid[0]), round(centroid[1]))
                        blank_image = copy.deepcopy(cache)
                        cv2.rectangle(blank_image, start_point, end_point, color, radio)

                # If used on "mouse" mode
                elif not args['use_numeric_paint'] and mouse_painting:
                    if center_mouse is not None:
                        print(center_mouse)
                        if listmouse[-2] is None:
                            cache = copy.deepcopy(blank_image)
                            start_point_mouse = center_mouse
                        else:
                            end_point_mouse = center_mouse
                            blank_image = copy.deepcopy(cache)
                            cv2.rectangle(blank_image, start_point_mouse, end_point_mouse, color, radio)

            # Draw a circle when pressing 'o' key
            elif key == ord('o'):
                # If used on "mask" mode
                if not args['use_numeric_paint'] and not mouse_painting:
                    # If the previous pressed key was not o, create a cache and save the starting point
                    if listkeys[-2] != ord('o'):
                        cache = copy.deepcopy(blank_image)
                        start_point = (round(centroid[0]), round(centroid[1]))
                    # If the previous pressed keys was an o, draw circle
                    else:
                        end_point = (round(centroid[0]), round(centroid[1]))
                        radius = int(((start_point[0] - end_point[0]) ** 2 + (start_point[1] - end_point[1]) ** 2)
                                     ** (1/2))
                        blank_image = copy.deepcopy(cache)
                        cv2.circle(blank_image, start_point, radius, color, radio)

                # If used on "mouse" mode
                elif not args['use_numeric_paint'] and mouse_painting:
                    if center_mouse is not None:
                        if listmouse[-2] is None:
                            cache = copy.deepcopy(blank_image)
                            start_point_mouse = center_mouse
                        else:
                            end_point_mouse = center_mouse
                            radius = int(((start_point_mouse[0] - end_point_mouse[0]) ** 2 + (start_point_mouse[1] -
                                      end_point_mouse[1]) ** 2) ** (1 / 2))
                            blank_image = copy.deepcopy(cache)
                            cv2.circle(blank_image, start_point_mouse, radius, color, radio)

        # If the thickness of the line is zero the program doesn't draw
        if radio == 0:
            pass
        else:
            # Painting with the mouse, not drawing rectangles or circles
            if isdown and mouse_painting and not key == ord('s') and not key == ord('o'):

                # If the user uses the shake prevention
                if shake_prevention_on:

                    # Calculate the distance between the point of the mouse pressed and the previous point
                    distance_mouse = math.sqrt(((center_mouse[0] - center_prev_mouse[0]) ** 2) + (
                            (center_mouse[1] - center_prev_mouse[1]) ** 2))

                    # If the distance is above a certain threshold
                    if distance_mouse > threshold:
                        # Defining the center_prev to use in the next cycle
                        center_prev_mouse = center_mouse
                    else:
                        # If the distance is below that threshold, paint a line according to the inputs
                        cv2.line(blank_image, center_prev_mouse, center_mouse, color, radio)
                        # Defining the center_prev to use in the next cycle
                        center_prev_mouse = center_mouse

                # If the user does not use the shake prevention mode
                else:
                    # Paint a line according to the inputs
                    cv2.line(blank_image, center_prev_mouse, center_mouse, color, radio)
                    # Defining the center_prev to use in the next cycle
                    center_prev_mouse = center_mouse

            # Painting with the mask, not drawing rectangles or circles
            elif not mouse_painting and not key == ord('s') and not key == ord('o'):

                # If no centroid is found, do not draw
                if centroid is None:
                    pass

                else:
                    # Change the variable centroid to a tuple
                    center = (int(centroid[0]), int(centroid[1]))

                    # If the user uses the shake prevention
                    if shake_prevention_on:

                        # Calculate the distance between the centroid detected and the previous centroid detected
                        distance = math.sqrt(((center[0] - center_prev[0]) ** 2) + ((center[1] - center_prev[1]) ** 2))

                        # If the distance is above a certain threshold
                        if distance > threshold:
                            # Defining the center_prev to use in the next cycle
                            center_prev = center
                        else:
                            # Paint a line according to the inputs
                            cv2.line(blank_image, center_prev, center, color, radio)
                            # Defining the center_prev to use in the next cycle
                            center_prev = center
                    else:
                        # Paint a line according to the inputs
                        cv2.line(blank_image, center_prev, center, color, radio)
                        # Defining the center_prev to use in the next cycle
                        center_prev = center

        # If you are on numeric paint mode
        if args['use_numeric_paint']:

            # If you press space bar, the program shuts down and delivers statistics
            if key & 0xFF == ord(' '):
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


        # Changing to real frame when "v" is pressed
        if real_toggle:
            # Replacing the white canvas with the real frame
            blend_image = createBlend(blank_image, frame)

            # Shows the real frame
            cv2.imshow("Canvas", blend_image)
        else:
            # Showing the white canvas
            cv2.imshow("Canvas", blank_image)
        # Show the webcam frame and the mask
        cv2.imshow("Original", frame)
        cv2.imshow("Mask", mask_original)

        # If you press q, the program shuts down
        if key & 0xFF == ord('q'):
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
