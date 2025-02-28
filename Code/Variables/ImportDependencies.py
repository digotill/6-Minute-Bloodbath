# Standard library imports
import copy  # For creating shallow and deep copies of objects
import traceback  # For printing or retrieving stack traces
import cProfile  # For deterministic profiling of Python programs
import os  # For interacting with the operating system
import ctypes  # For creating and manipulating C data types in Python
import logging  # For flexible event logging system for applications and libraries
import time  # For time-related functions
import functools  # For higher-order functions and operations on callable objects
import math  # For mathematical functions
import random  # For generating random numbers
import gc  # For garbage collection interface

# Third-party library imports
import pygame  # For game development
import moderngl  # For OpenGL rendering
import psutil  # For system and process utilities
import pandas as pd  # For data manipulation and analysis
import numpy as np  # For numerical operations
from pympler import asizeof  # For memory usage analysis
from perlin_noise import PerlinNoise  # For generating Perlin noise
from pygame.math import Vector2 as v2  # Vector2 class for 2D vector operations
from copy import deepcopy  # For creating deep copies of objects
from itertools import product  # For creating cartesian products of iterables
from pstats import Stats  # For profiling statistics


# Local imports
from Code.Shaders import Shader  # Custom shader module
from Code.Variables.LoadAssets import *  # Asset loading module
from Code.DataStructures.Timer import *  # Custom timer module
from Code.Utilities.Methods import *  # Utility methods module