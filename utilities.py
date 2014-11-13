import sys
import wave
import sys
import wave
import magic
from array import array
import tempfile
import os
import subprocess
import glob

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

def is_mp3(filepath):
    """
    Arguements: filepath
 
    Checks if a file is in MPEG format

    Returns TRUE if given file is MPEG. Otherwise returns false
    """
    real_path = os.path.realpath(filepath)
    header = subprocess.check_output(['file', '-b', real_path])
    if 'MPEG ADTS, layer III' in header:
        return True
    elif 'ID3' in header:
      audio = MP3(path)
      return 'audio/mp3' in audio.mime
    return False

def mp3_to_wav(filepath):
    """
    Arguements: filepath

    Converts mp3 to wav

    Returns the filepath of the converted file
    """
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
    data = []    
    if channel == 2:
        left = raw_data[0::2]
        right = raw_data[1::2]
        for i in range(0, len(left)):
             data.append((left[i] + right[i]) / 2)
    else:
        data = raw_data
    return data

def del_temp_files():
    """
     Arguements: None

    Deletes all temp files created by program
    """
    os.chdir('/tmp')
    files = glob.glob('*.wav')
    for filename in files:
        os.remove(filename)

#define normalize array function here

#define get FFT and powers function here

#define Euclidian distance function here
    
def compare(filepath1, filepath2):
    """
    Arguments: filepath x filepath
    
    Compares two WAVE files found at the base of a file path 
    
    Returns TRUE if the two files MATCH. Otherwise returns FALSE.
    """
    """
    -define cache
    -define new framerate
    -call function to normalize the int array of the song
    -call function to get fft and powers
    -store fft and powers in cache
    -call function to compare Euclidian distances

    REMOVE:
    -get rid of comparing arrays

    OPTIONS:
    -normalize volume
    """
    if is_mp3(filepath1):
        filepath1 = mp3_to_wav(filepath1)
    if is_mp3(filepath2):
        filepath2 = mp3_to_wav(filepath2)
    if get_length(filepath1) == get_length(filepath2):
        data1 = read_file(filepath1)
        array1 = string_to_array(data1, get_channel(filepath1))
        data2 = read_file(filepath2)
        array2 = string_to_array(data2, get_channel(filepath2))

    cache{}
    if filepath1 in cache:
        tuple1 = cache[filepath1]
        if filepath2 in cache:
            tuple2 = cache[filepath2]
        else
            norm_array2 = scipy.signal.resample(array2, 44100)
            tuple1 = get_FFT_Powers(norm_array2)
    else
        norm_array2 = scipy.signal.resample(array2, 44100)
        tuple1 = get_FFT_Powers(norm_array2)
 
    """
        i = 0
        threshold = len(array1) * .3        
        while (i < len(array1)) and (i < len(array2)):
            if not (array1[i] == 0):
                distance_var = abs(float(array2[i]) / float(array1[i]))
                if not (distance_var >= 0.7 and distance_var <= 1.5):
                    if (threshold == 0):
                        return False
                    threshold -= 1
            i += 1
        return True
    """
    else:
        return False
