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


cache = {}

# Returns the short name of the file
def get_file_name(path):
    return os.path.basename(os.path.normpath(path))


def get_file_path(file, dir):
    file_path = dir + '/' + file
    return file_path

def del_temp_files():
    """
     Arguements: None

    Deletes all temp files created by program
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
    
    Checks if a file is in WAVE or MPEG format.
    
    Returns TRUE if the given file IS a wave or mpeg file. Otherwise returns FALSE.
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
    f = wave.open(filepath, 'r')
    frate = f.getframerate()
    return frate

def read_file(filepath):
    f = wave.open(filepath, 'r')
    nframes = f.getnframes()
    data = f.readframes(nframes)
    return data

def get_nframes(filepath):
    f = wave.open(filepath, 'r')
    nframes = f.getnframes()
    return nframes

def compare_segs(seg1, seg2):
    segs_matched = 0
    if(len(seg1) == len(seg2)):
        for i in range(len(seg1)):
            if seg1[i] == seg2[i]:
                segs_matched += 1
    return segs_matched


def compare_fprints(fprint1, fprint2):
    seg_len1 = len(fprint1) - const.SEGMENT
    seg_len2 = len(fprint2) - const.SEGMENT
    for i in range(seg_len1):
        for j in range(seg_len2):
            seg1 = fprint1[i:i+const.SEGMENT-1]
            seg2 = fprint2[j:j+const.SEGMENT-1]
            nSegs_matched = compare_segs(seg1, seg2)
            #print nSegs_matched
            if nSegs_matched > const.THRESHOLD:
                return True
    return False

# Compares two files
def compare(path1, path2):

    fprint1 = []
    fprint2 = []

    if path1 not in cache:
        f = norm.normalize_wav(path1)

        nframes = get_nframes(f)
        frate = get_frate(f)
        chunk_size = frate / 10

        string = read_file(f)
        data = array.array('h', string)

        
        fprint1 = fp.get_fprint(data, frate, nframes)
        #fprint1 = fp.get_fprint(data1, chunk_size, nframes, frate)

        cache[path1] = fprint1
    else:
        fprint1 = cache[path1]
    
    if path2 not in cache:
        f = norm.normalize_wav(path2)

        nframes = get_nframes(f)
        frate = get_frate(f)
        chunk_size = frate / 10

        string = read_file(f)
        data = array.array('h', string)

        fprint2 = fp.get_fprint(data, frate, nframes)
        #fprint2 = fp.get_fprint(data1, chunk_size, nframes, frate)

        cache[path2] = fprint2
    else:
        fprint2 = cache[path2]

    return compare_fprints(fprint1, fprint2)

