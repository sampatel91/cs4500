import sys
import os
import wav
import audioop
import numpy
import numpy.fft
from scipy.fftpack.realtransforms import dct
from scipy.signal import lfilter, hamming

import utilities
from config import *



def normalize_wav(filepath):
    """
    Normalizes a .wav file to a single channel .wav file

   Args: filepath

   Returns: The normalized .wav file
    """"
    
