#!/usr/bin/python

import sys
import wave
import array
import os
import subprocess
import tempfile
import glob
import fingerprint as fp
import constants as const
import normalize as norm

# cache : stores processed files for future reference
cache = {}

def get_file_name(filepath):
    """
    Arguments: filepath

    Returns the file name found at the base of the given filepath.
    """
    return os.path.basename(os.path.normpath(filepath))

def get_file_path(file, dir):
    """
    Arguments: file name x directory

    Returns a filepath.
    """
    file_path = dir + '/' + file
    return file_path

def del_temp_files():
    """
    Arguments: None

    Deletes all temp files created by the application. 
    """
    os.chdir('/tmp')
    files = glob.glob('*.wav')
    for filename in files:
        os.remove(filename)


def check_args(args):
    """
    Arguments: Array of command line arguments
    
    Validates the command line arguments.
    
    Returns an error message to STDERR if the command line arguments 
    are invalid and exits the application.
    """
    if len(args) != 5:
        sys.stderr.write('ERROR: incorrect command line\n\n')
        sys.exit(-1)
    else:
        if not ((args[1] == '-f' or args[1] == '-d') and
                    (args[3] == '-f' or args[3] == '-d')):
            sys.stderr.write('ERROR: incorrect command line\n\n')
            sys.exit(-1)

def is_supported_file(filepath):
    """
    Arguments: filepath
    
    Checks if a file is in WAVE or MP3 format.
    
    Returns TRUE if the given file is in the correct audio format.
    Otherwise returns FALSE.
    """
    real_path = os.path.realpath(filepath)
    header = subprocess.check_output(['file', '-b',real_path])
    if 'MPEG ADTS, layer III' or 'WAVE audio' in header:
        return True
    else:
        sys.stderr.write('ERROR: %s is not a supported format\n' % (filepath))
        sys.exit(1)
    return False

def get_frate(filepath):
    """
    Arguments: filepath
    
    Computes and returns the frame rate of the audio file found at the base of
    the given filepath.
    """
    f = wave.open(filepath, 'r')
    frate = f.getframerate()
    return frate

def read_file(filepath):
    """
    Arguments: filepath

    Reads and returns the data of the audio file found at the base of the 
    given filepath.
    """
    f = wave.open(filepath, 'r')
    nframes = f.getnframes()
    data = f.readframes(nframes)
    return data

def get_nframes(filepath):
    """
    Arguments: filepath

    Computes and returns the number of frames of the audiofile found at the
    base of the given filepath.
    """
    f = wave.open(filepath, 'r')
    nframes = f.getnframes()
    return nframes

def compare_segs(seg1, seg2):
    """
    Arguments: Segment Array x Segment Array

    Compares the divided segments of audio files and returns the total number 
    of matching segments.
    """
    segs_matched = 0
    if(len(seg1) == len(seg2)):
        for i in range(len(seg1)):
            if seg1[i] == seg2[i]:
                segs_matched += 1
    return segs_matched


def compare_fprints(fprint1, fprint2):
    """
    Arguments: fingerprint array X fingerprint array

    Compares two audio file fingerprints and returns TRUE if the two have
    the required number of matching segments. Otherwise, FALSE.
    """
    seg_len1 = len(fprint1) - const.SEGMENT
    seg_len2 = len(fprint2) - const.SEGMENT
    for i in range(seg_len1):
        for j in range(seg_len2):
            seg1 = fprint1[i:i+const.SEGMENT-1]
            seg2 = fprint2[j:j+const.SEGMENT-1]
            nSegs_matched = compare_segs(seg1, seg2)
            if nSegs_matched > const.THRESHOLD:
                return True
    return False

def compare(path1, path2):
    """
    Arguments: filepath x filepath

    Compares two audio files and returns TRUE if the two are considered 
    a match. Otherwise, FALSE.
    """
    fprint1 = [] 
    fprint2 = []

    # Normalizes and computes needed data from path1 and stores it within 
    # the cache.
    if path1 not in cache:
        f = norm.normalize_wav(path1)

        nframes = get_nframes(f)
        frate = get_frate(f)
        chunk_size = frate / 10

        string = read_file(f)
        data = array.array('h', string)

        
        fprint1 = fp.get_fprint(data, frate, nframes, chunk_size)

        cache[path1] = fprint1
    else:
        fprint1 = cache[path1]
    
    # Normalizes and computes needed data from path2 and stores it within
    # the cache.
    if path2 not in cache:
        f = norm.normalize_wav(path2)

        nframes = get_nframes(f)
        frate = get_frate(f)
        chunk_size = frate / 10

        string = read_file(f)
        data = array.array('h', string)

        fprint2 = fp.get_fprint(data, frate, nframes, chunk_size)

        cache[path2] = fprint2
    else:
        fprint2 = cache[path2]

    return compare_fprints(fprint1, fprint2)

