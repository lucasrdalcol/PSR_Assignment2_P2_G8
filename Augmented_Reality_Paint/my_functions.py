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
from skimage.io import imread, imshow
from skimage.color import rgb2gray
from skimage.morphology import (erosion, dilation, closing, opening,
                                area_closing, area_opening)
from skimage.measure import label, regionprops, regionprops_table
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt


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
    """
    Toggle a variable after x seconds and untoggle it after 2x seconds
    :param start_time: Float32
    :param toggle: Bool
    :param seconds: Int
    :return:
    """
    # Measure elapsed time
    elapsed_time = toc(start_time)

    # If the elapsed time is divisible by the seconds variable, change the toggle variable
    if round(elapsed_time % seconds, 1) == 0:
        toggle = ~toggle
        # After changing the toggle, wait for 0.1 seconds, to avoid false toggles
        time.sleep(0.1)
    return toggle


def createBlend(white_image, frame):
    """
    Blend the canvas with the real frame, placing the drawings on top of the real image
    :param frame: Cv2 image - Uint8
    :param white_image: Cv2 image - Uint8
    :return frame: Cv2 image - Uint8
    """
    # Create mask of white pixels
    mask = cv2.inRange(white_image, np.array([255, 255, 255]), np.array([255, 255, 255]))
    mask = mask.astype(np.bool)

    # Placing the drawing in the original frame
    frame_cp = copy.deepcopy(frame)
    frame_cp[~mask] = white_image[~mask]

    return frame_cp


def findConnectedRegions(mask_original):
    """
    Create a mask with the largest blob of mask_original and return its centroid coordinates
    :param mask_original: Cv2 image - Uint8
    :return mask: Cv2 image - Bool
    :return centroid: List of 2 values
    """

    mask_original = cv2.cvtColor(mask_original, cv2.COLOR_BGR2GRAY)

    # Threshold it so it becomes binary
    ret, thresh = cv2.threshold(mask_original, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # You need to choose 4 or 8 for connectivity type
    connectivity = 4

    # Perform the operation
    output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)

    # Get the results
    # The first cell is the number of labels
    num_labels = output[0]

    # The second cell is the label matrix
    labels = output[1]

    # The third cell is the stat matrix
    stats = output[2]

    # The fourth cell is the centroid matrix
    centroids = output[3]

    centroids_coordinates = {}
    bounding_boxes = {}
    # For each blob, find the centroids
    for label in range(1, num_labels):
        # Find centroid
        centroids_coordinates[label] = centroids[label]
        bounding_boxes[label] = stats[label, :-1]

    return centroids_coordinates, bounding_boxes, labels


def mse(image_a, image_b):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compareImages(image_a, image_b):
    # compute the mean squared error and structural similarity
    # index for the images

    m = mse(image_a, image_b)
    s = ssim(image_a, image_b, multichannel=True)

    image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2RGB)
    image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2RGB)

    # setup the figure
    fig = plt.figure('Original and correct numeric paint x yours numeric paint')
    plt.suptitle(
        'Mean Square Error: ' + str(round(m, 2)) + ' , Structural Similarity: ' + str(round(s * 100, 2)) + ' %')

    # show first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(image_a, cmap=plt.cm.gray)
    plt.axis("off")

    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(image_b, cmap=plt.cm.gray)
    plt.axis("off")

    # show the images
    plt.show()

def drawNumericPaintImage(blank_image):
    # Create random lines in the blank image
    down_tol = 0.2
    up_tol = 0.8
    pts = [[0, randint(int(down_tol * blank_image.shape[0]), int(up_tol * blank_image.shape[0]))],
           [randint(int(down_tol * blank_image.shape[1]), int(blank_image.shape[1] / 2)),
            randint(int(down_tol * blank_image.shape[0]), int(up_tol * blank_image.shape[0]))],
           [randint(int(down_tol * blank_image.shape[1]), int(up_tol * blank_image.shape[1])), blank_image.shape[0]],
           [blank_image.shape[1], randint(int(down_tol * blank_image.shape[0]), int(up_tol * blank_image.shape[0]))],
           [randint(int(down_tol * blank_image.shape[1]), int(up_tol * blank_image.shape[1])), 0]]
    pts = np.array(pts)
    cv2.polylines(img=blank_image, pts=[pts], isClosed=True, color=(0, 0, 0), thickness=2)

    # Find the centroids of the regions to draw the color number
    centroids_coordinates, bounding_boxes, labeled_image = findConnectedRegions(blank_image)

    # Start variables
    region_colors = {}
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    # Draw region color idx
    for centroids_coordinates_key, centroid_coordinates_value in centroids_coordinates.items():
        random_idx = randint(1, 4)
        region_colors[centroids_coordinates_key] = {}
        region_colors[centroids_coordinates_key]['color_idx'] = random_idx
        region_colors[centroids_coordinates_key]['color'] = colors[random_idx - 1]
        blank_image = cv2.putText(blank_image, str(random_idx), (int(centroid_coordinates_value[0]),
                                                                 int(centroid_coordinates_value[1])),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)

    # Paint image to have the corrected image. After use this painted image to compare with our painting.
    painted_image = copy.deepcopy(blank_image)
    for region_color_key, region_color_value in region_colors.items():
        mask = labeled_image == region_color_key
        painted_image[mask] = region_color_value['color']

    return blank_image, painted_image