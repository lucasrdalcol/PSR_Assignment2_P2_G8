#!/usr/bin/python3

# --------------------------------------------------
# Import Modules
# --------------------------------------------------
import argparse
import numpy as np
import cv2.cv2 as cv2
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
#   - Emanuel Krzyszton
#   - João Pedro Tira Picos Costa Nunes
#
# PSR, University of Aveiro, November 2021.
# ---------------------------------------------------


def main():
    # ---------------------------------------------------
    # Initialization
    # ---------------------------------------------------
    #--------------------------------------------------
    # Create parser
    # --------------------------------------------------
    # ap = argparse.ArgumentParser()
    # ap.add_argument('-j', '--json', required=True, help="Definition of test mode")
    # args = vars(ap.parse_args())

    # --------------------------------------------------
    # Setting up the painting interface. White blank image.
    # --------------------------------------------------
    blank_image = 255 * np.ones(shape=[480, 640], dtype=np.uint8)
    cv2.imshow("White Blank", blank_image)

    # --------------------------------------------------
    # Video capture
    # --------------------------------------------------
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        cv2.imshow("Original: ", frame)
        # If you press q, the program shuts down and saves the final directory
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

    # --------------------------------------------------
    # Loading Json file
    # --------------------------------------------------


if __name__ == "__main__":
    main()
