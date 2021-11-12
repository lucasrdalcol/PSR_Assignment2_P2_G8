#!/usr/bin/python3

# --------------------------------------------------
# IMPORT MODULES
# --------------------------------------------------
from collections import namedtuple
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
##   DATA STRUCTURES   ##
# ------------------------


# ------------------------
## FUNCTION DEFINITION ##
# ------------------------
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
