import sys
import wave
import magic
from array import array

def checkArgs(args):
    if len(args) != 5:
        sys.stderr.write('ERROR: Proper command line usage is one of:\n')
        sys.stderr.write(' ./dan -f <pathname> -f <pathname>\n')
        sys.stderr.write(' ./dan -f <pathname> -d <pathname>\n')
        sys.stderr.write(' ./dan -d <pathname> -f <pathname>\n')
        sys.stderr.write(' ./dan -d <pathname> -d <pathname>\n')
        sys.exit(-1)
    else:
        if not ((args[1] == '-f' or args[1] == '-d') and
                    (args[3] == '-f' or args[3] == '-d')):
            sys.stderr.write('ERROR: Proper command line usage is one of:\n')
            sys.stderr.write(' ./dan -f <pathname> -f <pathname>\n')
            sys.stderr.write(' ./dan -f <pathname> -d <pathname>\n')
            sys.stderr.write(' ./dan -d <pathname> -f <pathname>\n')
            sys.stderr.write(' ./dan -d <pathname> -d <pathname>\n')
            sys.exit(-1)


def getFileName(file):
    fileName = file.split('/')
    if len(fileName) == 0:
        return fileName
    else:
        return fileName[len(fileName) - 1]


def is_wave_file(filename):
    mime = magic.open(magic.MIME_TYPE)
    mime.load()
    if mime.file(filename) == ('audio/x-wav'):
        return True
    else:
        return False


def get_length(file):
    file = wave.open(file, 'r')
    frames = file.getnframes()
    frate = file.getframerate()
    duration = frames / frate
    return duration


def read_file(file):
    file = wave.open(file, 'r')
    frames = file.getnframes()
    data = file.readframes(frames)
    return data


def get_channel(file):
    file = wave.open(file, 'r')
    return file.getnchannels()


def string_to_array(string, channel):
    raw_data = array('h', string)
    if channel == 2:
        left = raw_data[0::2]
        right = raw_data[1::2]
        for i in range(0, len(left)):
            data = [(left[i] + right[i]) / 2]
    else:
        data = raw_data
    return data

def compare(file1, file2):
    data1 = read_file(file1)
    array1 = string_to_array(data1, get_channel(file1))
    data2 = read_file(file2)
    array2 = string_to_array(data2, get_channel(file2))
    i = 0
    while i < len(array1):
        if not (array1[i] == array2[i]):
	    return False
        i += 1
    return True

