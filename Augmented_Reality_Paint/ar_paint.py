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

install_extras(['python'])
set_default_style('light')
draw = False
point1 = ()
point2 = ()
ix, iy = -1, -1
radius = 0


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


def draw_rectangle(event, x, y, flags, params):
    global point1, point2, draw, cache, blank_image

    if event == cv2.EVENT_LBUTTONDOWN:
        if draw is False:
            draw = True
            point1 = (x, y)
            point2 = (x, y)
            cache = copy.deepcopy(blank_image)
        else:
            draw = False

    elif event == cv2.EVENT_MOUSEMOVE:
        if draw is True:
            point2 = (x, y)
            blank_image = copy.deepcopy(cache)

    elif event == cv2.EVENT_LBUTTONUP:
        if draw is True:
            point2 = (x, y)


# Create a function based on a CV2 Event (Left button click)
def draw_circle(event, x, y, flags, param):
    global ix, iy, draw, radius, blank_image, cache

    if event == cv2.EVENT_LBUTTONDOWN:
        draw = True
        # we take note of where that mouse was located
        ix, iy = x, y
        cache = copy.deepcopy(blank_image)

    elif event == cv2.EVENT_MOUSEMOVE:
        draw = True
        blank_image = copy.deepcopy(cache)

    elif event == cv2.EVENT_LBUTTONUP:
        radius = int(math.sqrt(((ix - x) ** 2) + ((iy - y) ** 2)))
        cv2.circle(video_capture, (ix, iy), radius, (0, 0, 255), thickness=1)
        draw = False


def onMouse(event, x, y, flags, param, draw, rect, circ):
    global isdown
    global center_mouse
    global cache
    global blank_image
    global drect
    global point1, point2
    global ix, iy
    global dcirc

    print("Draw: "+ str(draw))
    print("Rectangle: "+str(rect))
    print("Circle: "+str(circ))

    if event == cv2.EVENT_MOUSEMOVE:
        if draw:
            if isdown:
                center_mouse = (x, y)
        elif rect:
            if drect is True:
                point2 = (x, y)
                blank_image = copy.deepcopy(cache)
        elif circ:
            if dcirc is True:
                ix, iy = (x, y)
                blank_image = copy.deepcopy(cache)

    if event == cv2.EVENT_LBUTTONDOWN:
        if draw:
            isdown = True
            center_mouse = (x, y)
        elif rect:
            print('Left Button')
            if drect is False:
                drect = True
                point1 = (x, y)
                point2 = (x, y)
                cache = copy.deepcopy(blank_image)
            else:
                drect = False
        elif circ:
            print('Left button circle')
            if dcirc is False:
                dcirc = True
                ix, iy = (x,y)
                cache = copy.deepcopy(blank_image)
            else:
                dcirc = False

    if event == cv2.EVENT_LBUTTONUP:
        if draw:
            isdown = False
        elif rect:
            if drect is True:
                point2 = (x, y)
        elif circ:
            if dcirc is True:
                ix, iy = (x, y)

    if rect:
        if point1 and point2:
            print('Drawing rectangle')
            cv2.rectangle(blank_image, point1, point2, (0, 255, 0))

    if circ:
        if ix and iy:
            print('Drawing circle')
            cv2.circle(blank_image, (ix,iy), radius , (0,0,255),1)


def main():
    # ---------------------------------------------------
    # Initialization
    # ---------------------------------------------------
    # Starting global variables
    global numeric_paint_blank_image, painted_image, isdown, drect, center_mouse, video_capture, cache, blank_image, dcirc

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

    cache = copy.deepcopy(blank_image)

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



    # Setting up variables
    circ = False
    dcirc = False
    rect = False
    drect = False

    real_toggle = False
    isdown = False
    mouse_painting = True
    radio = 5
    # global color
    color = (255, 0, 0)
    color_str = 'BLUE'
    center = (200, 200)
    center_mouse = (200, 200)
    center_prev = (200, 200)
    center_prev_mouse = (200, 200)

    cv2.imshow("Canvas", blank_image)
    # onMouseDefault = partial(onMouse, draw=mouse_painting, rect=rect)
    # cv2.setMouseCallback("Canvas", onMouseDefault)

    if args['use_shake_prevention']:  # if the user uses the shake prevention
        print(Fore.BLUE + Back.WHITE + 'You are using shake prevention.' + Style.RESET_ALL)
        shake_prevention_on = 1
    else:
        shake_prevention_on = 0

    print('You started your paint with color ' + Fore.BLUE + color_str + Fore.RESET + ' and pencil size ' + Fore.GREEN +
          str(radio) + Fore.RESET + ' as default parameters. \nYou started painting with the mouse. \nPress ' + Fore.RED + '"n"' + Style.RESET_ALL + ' to paint with the mask. \nPress ' + Fore.RED + '"m"' + Style.RESET_ALL + ' to paint with the mouse again.\nPress ' + Fore.RED + '"v"' + Style.RESET_ALL + ' to toggle between the white canvas and the real frame.')

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
        key = cv2.waitKey(1)

        # if a key is pressed
        if key != -1:

            # Choose the color blue if "b" is pressed.
            if key == ord('b'):
                color = (255, 0, 0)
                color_str = 'BLUE'
                print(Fore.BLUE + color_str + ' color selected.                                   ' + Style.RESET_ALL, end='\r')

            # Choose the color green if "g" is pressed.
            elif key == ord('g'):
                color = (0, 255, 0)
                color_str = 'GREEN'
                print(Fore.GREEN + color_str + ' color selected.                                ' + Style.RESET_ALL, end='\r')

            # Choose the color red if "r" is pressed.
            elif key == ord('r'):
                color = (0, 0, 255)
                color_str = 'RED'
                print(Fore.RED + color_str + ' color selected.                                      ' + Style.RESET_ALL, end='\r')

            # Increase the pencil size if "+" is pressed.
            elif key == ord('+'):
                radio = radio + 1
                print('Pencil size is now ' + Fore.GREEN + str(radio) + Style.RESET_ALL + '                               ', end='\r')

            # Decrease the pencil size if "-" is pressed.
            elif key == ord('-'):
                radio = radio - 1
                if radio < 0:
                    radio = 0
                print('Pencil size is now ' + Fore.RED + str(radio) + Style.RESET_ALL + '                              ', end='\r')

            # Paint with the mouse if "m" is pressed.
            elif key == ord('m'):
                mouse_painting = True
                print('You pressed "m". You are painting with the mouse.             ', end='\r')

            # Paint with the mask if "n" is pressed.
            elif key == ord('n'):
                mouse_painting = False
                print('You pressed "n".You are painting with the mask.                ', end='\r')

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
                    blank_image = numeric_paint_blank_image
                print('\nYou pressed "c": The window "Canvas" was cleared.')

            # Save the current image if "w" is pressed.
            elif key == ord('w'):
                date = ctime()
                cv2.imwrite('drawing_' + date + '.png', blank_image)
                print('\nCurrent image saved as: ' + Fore.BLUE + 'drawing_' + date + '.png' + Style.RESET_ALL)

            # Draw a rectangle when pressing 's' key
            elif key == ord('s'):
                rect = not rect
                if rect:
                    circ = False
                    mouse_painting = False
                    print('You pressed "s".You are drawing a rectangle.                ', end='\r')

            # Draw a circle when pressing 'o' key
            elif key == ord('o'):
                circ = not circ
                if circ:
                    rect = False
                    mouse_painting = False
                    print("You pressed 'o'. You are drawing a circle.                ", end='\r')

        if radio == 0:  # if the thickness of the line is zero the program doesn't draw
            pass
        else:
            if mouse_painting:  # Code for when the user is pressing the mouse
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

        if args['use_numeric_paint']:
            # If you press space bar, the program shuts down
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

        # Defining mouse callback
        onMouseDefault = partial(onMouse, draw=mouse_painting, rect=rect, circ=circ)
        cv2.setMouseCallback("Canvas", onMouseDefault)


        # Changing to real frame
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
