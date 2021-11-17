#!/usr/bin/python3

# --------------------------------------------------
# IMPORT MODULES
# --------------------------------------------------
import copy
from collections import namedtuple

import cv2
import numpy as np
from colorama import Fore
from numpy.random import randint
import time
from my_classes import *
import readchar
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pprint import pformat


# ------------------------
# Data Structures
# ------------------------


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


def tic():
    """
    Functions used to return the numbers of seconds passed since epoch to use with function toc() afterwards.
    Like tic toc matlab functions.
    :return start_time: a float.
    """

    # Get the number os seconds passed since epoch
    start_time = time.time()

    return start_time


def toc(start_time):
    """
    Function used to return the elapsed time since function tic() was used. tic() and toc() works together.
    :param start_time: number of seconds passed since epoch given by tic() function. Datatype: float
    :return elapsed_time: a float.
    """

    # Get the number of seconds passed since epoch and subtract from tic(). This is the elapsed time from tic to toc.
    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time


def pprint_color(obj):
    """
    Function that return the pretty print with colors.
    :param obj: the string that should be printed.
    """
    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()))


def createMask(ranges, image):
    """
    Using a dictionary wth ranges, create a mask of an image respecting those ranges
    :param ranges: Dictionary generated in color_segmenter.py
    :param image: Cv2 image - UInt8
    :return mask: Cv2 image - UInt8
    """

    # Create an array for minimum and maximum values
    mins = np.array([ranges['B']['min'], ranges['G']['min'], ranges['R']['min']])
    maxs = np.array([ranges['B']['max'], ranges['G']['max'], ranges['R']['max']])

    # Create a mask using the previously created array
    mask = cv2.inRange(image, mins, maxs)

    return mask


def findCentroid(mask_original):
    """
    Create a mask with the largest blob of mask_original and return its centroid coordinates
    :param mask_original: Cv2 image - Uint8
    :return mask: Cv2 image - Bool
    :return centroid: List of 2 values
    """

    # Defining maximum area and mask label
    maxArea = 0
    maxLabel = 0

    # You need to choose 4 or 8 for connectivity type
    connectivity = 4

    # Perform the operation
    output = cv2.connectedComponentsWithStats(mask_original, connectivity, cv2.CV_32S)

    # Get the results
    # The first cell is the number of labels
    num_labels = output[0]

    # The second cell is the label matrix
    labels = output[1]

    # The third cell is the stat matrix
    stats = output[2]

    # The fourth cell is the centroid matrix
    centroids = output[3]

    # For each blob, find their area and compare it to the largest one
    for label in range(1, num_labels):
        # Find area
        area = stats[label, cv2.CC_STAT_AREA]

        # If the area is larger then the max area to date, replace it
        if area > maxArea:
            maxArea = area
            maxLabel = label

    # If there are blobs, the label is different than zero
    if maxLabel != 0:
        # Create a new mask and find its centroid
        mask = labels == maxLabel
        centroid = centroids[maxLabel]
    else:
        # If there are no blobs, the mask stays the same, and there are no centroids
        mask = mask_original
        centroid = None

    return mask, centroid


def greenBlob(image, mask):
    """
    Using a mask, create a green undertone to an image
    :param image: Cv2 image - Uint8
    :param mask: Cv2 image - Bool
    :return image: Cv2 image - Uint8
    """

    # Determine image size
    h, w, _ = image.shape

    # Creating colour channels, using the mask as the green one
    b = np.zeros(shape=[h, w], dtype=np.uint8)
    g = mask.astype(np.uint8) * 255
    r = copy.deepcopy(b)

    # Merge the channels to create a green mask
    image_green = cv2.merge([b, g, r])

    # Blend the image with the green mask
    image = cv2.addWeighted(image, 1, image_green, 0.2, 0)

    return image


def periodDefinition(start_time, toggle, seconds):

    elapsed_time = toc(start_time)
    print(round(elapsed_time % seconds, 1))
    if round(elapsed_time % seconds, 1) == 0:
        toggle = ~toggle
        time.sleep(0.1)
    return toggle
