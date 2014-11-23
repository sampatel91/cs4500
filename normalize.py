import sys
import os
import tempfile
import constants as const

import subprocess

TEMP_FOLDER = []

def get_resample_cmd(src, dest):
    cmd = '/course/cs4500f14/bin/lame --resample 16 -m m -b 16 --silent %s %s' % (src, dest)
    return cmd

def get_decode_cmd(src, dest):
    cmd = '/course/cs4500f14/bin/lame --decode --silent --mp3input %s %s' % (src, dest)
    return cmd

def normalize_wav(filepath):
    """
    Normalizes a .wav file to a single channel .wav file

    Args: filepath

    Returns: The normalized .wav file

    """

    temp_file, temp_path = tempfile.mkstemp(dir='/tmp')
    command1 = get_resample_cmd(filepath, temp_path)
    subprocess.call(command1, shell=True)
    
    temp_file2, temp_path2 = tempfile.mkstemp(dir='/tmp')
    command2 = get_decode_cmd(temp_path, temp_path2)
    subprocess.call(command2, shell=True)
    return temp_path2
