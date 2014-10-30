import sys
import wave
import magic
import numpy
import math
import struct
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

def get_file_path(file, dir):
    file_path = dir + '/' + file
    return file_path

def is_supported_file(filepath):
    """
    Arguments: filepath
    
    Checks if a file is in WAVE format.
    
    Returns TRUE if the given file IS a wave file. Otherwise returns FALSE.
    """
    """
    mime = magic.open(magic.MIME_TYPE)
    mime.load()
    if mime.file(filepath) == ('audio/x-wav') or mime.file(filepath) == ('audio/mpeg'):
        return True
    else:
        sys.stderr.write('ERROR: %s is not a supported format\n' % (filepath))
        sys.exit(1)
    """
    header = subprocess.check_output(['file', '-b', filepath])
    if 'MPEG ADTS, layer III' or 'WAVE' in header:
	return True
    return False

def is_mp3(filepath):
    header = subprocess.check_output(['file', '-b', filepath])
    if 'MPEG ADTS, layer III' in header:
	return True
    elif 'ID3' in header:
      audio = MP3(path)
      return 'audio/mp3' in audio.mime
    return False

def mp3_to_wav(filepath):
    f = tempfile.mkstemp(suffix='.wav')
    cmd = '/course/cs4500f14/bin/lame --decode --silent %s %s' % (filepath, f[1])
    subprocess.call(cmd, shell=True)
    return f[1]

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
    #data = struct.unpack('{n}h'.format(n=len(string)/2), string)
    data = []    
    if channel == 2:
        left = raw_data[0::2]
        right = raw_data[1::2]
        #print left
        #print right
        for i in range(0, len(left)):
             data.append((left[i] + right[i]) / 2)
             #print data[i]
#        data = [(left[i] + right[i]) / 2 for i in range(0, len(left))]
    else:
        data = raw_data
#    return abs(numpy.fft.rfft(data))
    #print data
    return data

def del_temp_files(filepath1, filepath2):
    if 'tmp' in filepath1:
	os.remove(filepath1)
    if 'tmp' in filepath2:
        os.remove(filepath2)

def compare(filepath1, filepath2):
    """
    Arguments: filepath x filepath
    
    Compares two WAVE files found at the base of a file path 
    
    Returns TRUE if the two files MATCH. Otherwise returns FALSE.
    """
    if is_mp3(filepath1):
	filepath1 = mp3_to_wav(filepath1)
        #mp3_wave = subprocess.check_output('file', '-b', filepath1)
        #print mp3_wav
    if is_mp3(filepath1):
	filepath2 = mp3_to_wav(filepath2)
        #mp3_wave2 = subprocess.check_output('file', '-b', filepath2)
        #print mp3_wav2
    #print filepath1
    #print filepath2
    if get_length(filepath1) == get_length(filepath2):
        data1 = read_file(filepath1)
        array1 = string_to_array(data1, get_channel(filepath1))
        data2 = read_file(filepath2)
        array2 = string_to_array(data2, get_channel(filepath2))
        #diff = numpy.corrcoef(array1, array2)
        #print diff
	"""if diff[0][1] > 0.9:
	    return True
	else:
	    return False
        diff = numpy.allclose(array1, array2)
        if diff:
            return True
        else:
            return False
        """
        #print array1
        #print array2
        i = 0
        threshold = len(array1) * .3        
        #print (len(array1))
        #print (len(array2))
        while (i < len(array1)) and (i < len(array2)):
	    if not (array1[i] == 0):
               # print array1[i]
               # print array2[i]
               # print threshold
                distance_var = (float(array2[i]) / float(array1[i]))
               # print distance_var
                if not (distance_var >= 0.8 and distance_var <= 1.5):
                    if (threshold == 0):
                        return False
	            threshold -= 1
            i += 1
        del_temp_files(filepath1, filepath2)
        return True
    else:
        del_temp_files(filepath1, filepath2)
        return False
