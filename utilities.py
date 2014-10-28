import sys
import wave
import magic
from array import array
import tempfile
import os
import subprocess

def check_args(args):
    """
    Arguments: Array of command line arguments
    
    Validates the command line arguments.
    
    Returns an error message to STDERR if the command line arguments are invalid and exits the application.
    """
    if len(args) != 5:
        sys.stderr.write('ERROR: incorrect command line\n\n')
        sys.exit(-1)
    else:
        if not ((args[1] == '-f' or args[1] == '-d') and
                    (args[3] == '-f' or args[3] == '-d')):
            sys.stderr.write('ERROR: incorrect command line\n\n')
            sys.exit(-1)


def get_file_name(filepath):
    """
    Arguments: filepath
    
    Returns the resource file name found at the end of the given file path
    """
    file_name = filepath.split('/')
    if len(file_name) == 0:
        return file_name
    else:
        return file_name[len(file_name) - 1]


def is_supported_file(filepath):
    """
    Arguments: filepath
    
    Checks if a file is in WAVE format.
    
    Returns TRUE if the given file IS a wave file. Otherwise returns FALSE.
    """
    mime = magic.open(magic.MIME_TYPE)
    mime.load()
    if mime.file(filepath) == ('audio/x-wav') or mime.file(filepath) == ('audio/mpeg'):
        return True
    else:
        sys.stderr.write('ERROR: %s is not a supported format\n' % (filepath))
        sys.exit(1)
 
def mp3_to_wav(filepath):
    wav = get_file_name(filepath.split('.')[0]) + '.wav'
    cmd = '/course/cs4500f14/bin/lame --decode %s tmp/%s' % (filepath, wav)
    subprocess.call(cmd, shell=True)
     

def get_length(filepath):
    """
    Arguments: filepath
    
    Returns the length of a WAVE file. 
    """
    file = wave.open(filepath, 'r')
    frames = file.getnframes()
    frate = file.getframerate()
    duration = frames / frate
    return duration


def read_file(filepath):
    """ 
    Arguments: filepath
    
    Returns the raw data within the given WAVE file.
    """
    file = wave.open(filepath, 'r')
    frames = file.getnframes()
    data = file.readframes(frames)
    return data


def get_channel(filepath):
    """
    Argument: filepath

    Returns 1 for mono and 2 for stereo channels.
    """
    file = wave.open(filepath, 'r')
    return file.getnchannels()


def string_to_array(string, channel):
    """
    Arguments: string x channel
    
    Returns an array of WAVE file channels.
    """
    raw_data = array('h', string)
    if channel == 2:
        left = raw_data[0::2]
        right = raw_data[1::2]
        for i in range(0, len(left)):
            data = [(left[i] + right[i]) / 2]
    else:
        data = raw_data
    return data

def compare(filepath1, filepath2):
    """
    Arguments: filepath x filepath
    
    Compares two WAVE files found at the base of a file path 
    
    Returns TRUE if the two files MATCH. Otherwise returns FALSE.
    """
    data1 = read_file(filepath1)
    array1 = string_to_array(data1, get_channel(filepath1))
    data2 = read_file(filepath2)
    array2 = string_to_array(data2, get_channel(filepath2))
    i = 0
    while i < len(array1):
        distance_var = array2[i] / array1[i]
        if not (distance_var >= 0.97 and distance_var <= 1.03):
	    return False
        i += 1
    return True
