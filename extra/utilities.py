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
import numpy
import scipy.io.wavfile
import scipy.signal
import audioop
import math
import constants
from operator import itemgetter
import scipy.signal
import audioop
import math


LAME = os.path.normpath('/course/cs4500f14/bin/lame')

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


def get_file_name(filepath):
    """
    Arguments: filepath
    
    Returns the resource file name found at the end of the given file 
    path
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
    cmd = '/course/cs4500f14/bin/lame --decode --mp3input --silent %s %s' % (filepath, f[1])
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

def get_frame_rate(filepath):
    file = wave.open(filepath, 'r')
    frate = file.getframerate()
    return frate

def read_file(filepath):
    """ 
    Arguments: filepath
    
    Returns the raw data within the given WAVE file.
    """
    #file = wave.open(filepath, 'r')
    #frames = file.getnframes()
    #data = file.readframes(frames)
    rate, data = scipy.io.wavfile.read(filepath)
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

#define apply hamming window
def apply_hamming(signal, window):
    result = []
    winLen = len(window)
    for sample in signal:
        samLen = len(sample)
        if samLen < winLen:
            sample = list(sample)
            sample[samLen:winLen] = [0] * (winLen - samLen)
            sample = tuple(sample)
        result.append(sample * window)
    return result

#define normalize array function here
def frame_sig(signal, samples_perframe):
    i = 0
    overlap = samples_perframe * 0.25
    framed_signal = []
    length = len(signal)
    while i < length:
        framed_signal.append(signal[i:int(i + samples_perframe)])
        i = int(i + samples_perframe - overlap)
    return framed_signal
        
#define get FFT and powers function here
def get_FFT_Powers(sig):

    """
    Arguments: signal

    Computes the Power Spectrum and FFT of a signal.
  
    Returns a tuple of FFTs and Powers of the given signal.
    """
    power_vals, fft_vals = [], []

    for frame in sig:
        if (len(frame) == 0): 
            break
        our_fft = numpy.fft.fft(frame)
        power = abs(our_fft) ** 2
        power_vals.append(power)
        fft_vals.append(our_fft)

    return (fft_vals, power_vals)

# define filterbank
def compute_filterbank(numfilter, fft_size, sample):
    
    highest_freq = sample / 2

    lowest_freq = 0

    # Covnvert our frequencies to their mel scale equivalent.
    high_mel = freq_2_mel_conversion(highest_freq)

    low_mel = freq_2_mel_conversion(lowest_freq)

    mel_interval = numpy.linspace(low_mel, high_mel, numfilter + 2)
    bin_fft = numpy.floor((fft_size + 1) * mel_2_freq_conversion(mel_interval) / sample)
    filter_bank = numpy.zeros([numfilter, fft_size])

    # Populate our filterbank in accordance with bin_fft
    for x in xrange(0, numfilter):
        for y in xrange(int(bin_fft[x]), int(bin_fft[x + 1])):
            filter_bank[x, y] = (y - bin_fft[x]) / (bin_fft[x + 1] - bin_fft[x])
        for y in xrange(int(bin_fft[x + 1]), int(bin_fft[x + 2])):
            filter_bank[x, y] = (bin_fft[x + 2] - y) / (bin_fft[x + 2] - bin_fft[x + 1])
    return filter_bank
    """
    numBands = int(numCoefficients)
    maxMel = int(freqToMel(maxHz))
    minMel = int(freqToMel(minHz))

    # Create a matrix for triangular filters, one row per filter
    filterMatrix = numpy.zeros((numBands, blockSize))

    melRange = numpy.array(xrange(numBands + 2))

    melCenterFilters = melRange * (maxMel - minMel) / (numBands + 1) + minMel

    # each array index represent the center of each triangular filter
    aux = numpy.log(1 + 1000.0 / 700.0) / 1000.0
    aux = (numpy.exp(melCenterFilters * aux) - 1) / 22050
    aux = 0.5 + 700 * blockSize * aux
    aux = numpy.floor(aux)  # Arredonda pra baixo
    centerIndex = numpy.array(aux, int)  # Get int values

    for i in xrange(numBands):
        start, centre, end = centerIndex[i:i + 3]
        k1 = numpy.float32(centre - start)
        k2 = numpy.float32(end - centre)
        up = (numpy.array(xrange(start, centre)) - start) / k1
        down = (end - numpy.array(xrange(centre, end))) / k2

        filterMatrix[i][start:centre] = up
        filterMatrix[i][centre:end] = down

    return filterMatrix.transpose()
    """
# define freq_2_mel_conversion
def freq_2_mel_conversion(freq):
    mel_convert = numpy.log(1 + freq / 700) * 1127.01048

    return mel_convert

# define mel_2_freq_conversion
def mel_2_freq_conversion(mel):
    freq_convert = (10 ** (mel / 1127.01048 - 1)) * 700
    #freq_convert = (math.exp(mel / 1127.01048 -1)) * 700 
    return freq_convert

# define mel filter bank
def apply_filterbank(powerSpec, filterbank):
    filtered_spec = []
    for x in xrange(0, len(powerSpec)):
        filtered_spec.append(numpy.dot(filterbank, powerSpec[x]))
    return_filtered_spec = numpy.log10(filtered_spec)
    return return_filtered_spec

#define get mfcc
def get_mfcc(filterSpec):
    mfcc = []
    for i in xrange(0, len(filterSpec)):
        mfcc.append(scipy.fftpack.dct(filterSpec[i][4:], norm='ortho')[:12])
    return mfcc

#define compare_fft_vals
def compare_fft_vals(sig1, sig2):
    diff = 0
    if len(sig1) > len(sig2):
        for i in range(len(sig2)):
            dist = (sig1[i] - sig2[i]) ** 2
            diff = diff + dist
    else:
        for i in range(len(sig1)):
            dist = (sig1[i] - sig2[i]) ** 2
            diff = diff + dist
    return diff

#define Euclidian distance function here
def compare_euclid(sig1, sig2, type):
    result = []
    length1 = len(sig1)
    length2 = len(sig2)
    comp = 0
    if type == 'mfcc':
        comp = 7
    elif type == 'fft':
        comp = 1e+11
    if length1 > length2:
        for i in range(len(sig2)):
            distance = compare_fft_vals(sig1[i], sig2[i])
            if abs(distance) < comp:
                result.append(distance)
    else:
        for i in range(len(sig1)):
            distance = compare_fft_vals(sig1[i], sig2[i])
            """
            diff = 0
            sub_sig1 = sig1[i]
            sub_sig2 = sig2[i]
            if len(sub_sig1) > len(sub_sig2):
                for i in range(len(sub_sig2)):
                    dist = (sub_sig1[i] - sub_sig2[i]) ** 2
                    diff = diff + dist
            else:
                for i in range(len(sub_sig1)):
                    dist = (sub_sig1[i] - sub_sig2[i]) ** 2
                    diff = diff + dist
#                    distance = eDist(sig1[i], sig2[i])
            """
            if abs(distance) < comp:
                result.append(distance)

    return result

#define normalize wave file
def norm_wave(filepath):
    f, fpath = tempfile.mkstemp(dir='/tmp', suffix='.wav')
#    command = [LAME, '--decode', '--silent', '--resample', '-m', 'm', '-b',
#    '16', filepath, fpath]
    cmd = '%s --quiet --resample 16 -m m -b 16 %s %s' % (LAME, filepath, fpath)
    subprocess.call(cmd, shell=True)
#    print cmd
    """
    try:
        subprocess.check_call(command)
    except:
        sys.stderr.write('ERROR')
        sys.exit(-1)
    """
    """ 
    f2, f2path = tempfile.mkstemp(dir='/tmp', suffix='.wav')
    f_norm = wave.open(f2path, 'wb')
    f_norm.setparams((1,2, 16000, nframes, 'NONE', 'NONE'))
    if nchannels != 1:
        frames = audioop.tomono(frames, 2, 1, 1)
    f_norm.writeframes(frames)
    f_norm.close()
    """
    return fpath

#define compare distance function
def comp_distance(sig1, sig2, type):
    #print("inside of comp_distance")
    distances = compare_euclid(sig1, sig2, type)
    sigLen1 = len(sig1)
    sigLen2 = len(sig2)
    #print distances
    if sigLen1 > sigLen2:
        if type == 'mfcc':
            prop = float(len(distances))/float(sigLen2)
        else:
            prop = (float(len(distances))/float(sigLen2)) * 10
    else:
        if type == 'mfcc':
            prop = float(len(distances))/float(sigLen1)
        else:
            prop = (float(len(distances))/float(sigLen1)) * 10
    print "Prop: %.5f" % prop
    if prop > 0.1:
        #print ("distance matched")
        return 1

#    print prop
    return 0


    """
    nparray1 = numpy.array(sig1)
    nparray2 = numpy.array(sig2)
    shorter = sig1
    longer = sig2
    i = 0 
    j = 0 
    j_prev = 0 

    while i < len(shorter):

        if j == len(longer) or len(shorter) - i > len(longer) - j:
            return 0

        if ((nparray1[i] - nparray2[j]) ** 2) < match_threshold:
            if i == 0:
                j_prev = j
            i += 1
            j += 1

        else:
            i = 0
            j = j_prev + 1
            j_prev = j

    return 1 
    """
def get_fft(signal):
    ffts =[]
    fft = numpy.fft.rfft(signal)
    for sample in fft:
        x = abs(sample)
        ffts.append(x)
    return ffts

def get_peak(ffts):
    return max(enumerate(ffts), key=itemgetter(1))[0]

def get_fprint(data, frate, nframes):
    result = []
    weight = 20
    chunk_size = frate/ 10
    for i in range(0, nframes, chunk_size):
        chunk_data = data[i:i+chunk_size]
        ffts = get_fft(chunk_data)
        peak_val = get_peak(ffts) * frate / len(chunk_data)
        print peak_val
        weight -= 1
        result.append(peak_val)
    return result

def compare_segs(seg1, seg2):
    segs_matched = 0
    if (not len(seg1) == len(seg2)):
        print "lenghts of segs diff"
        return 0
    for i in range(len(seg1)):
        if seg1[i] == seg2[i]:
            segs_matched = segs_matched + 1
#    for i in seg1:
#        for j in seg2:
            #print '%s == %s' % (i, j)
#            if i == j:
#                segs_matched += 1
    return segs_matched

def compare_fprints(fprint1, fprint2):
    seg_len1 = len(fprint1) - constants.SEGMENT
    seg_len2 = len(fprint2) - constants.SEGMENT
    for i in range(seg_len1):
        for j in range(seg_len2):
            seg1 = fprint1[i:i+constants.SEGMENT-1]
            seg2 = fprint2[j:j+constants.SEGMENT-1]
            nSegs_matched = compare_segs(seg1, seg2)
            #print nSegs_matched
            if nSegs_matched > constants.THRESHOLD:
                return True
    return False

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
    
#    if get_length(filepath1) == get_length(filepath2):
    """
    print filepath1
    print filepath2
    filepath1 = norm_wave(filepath1)
    filepath2 = norm_wave(filepath2)
    #print filepath1
    #print filepath2    
    if is_mp3(filepath1):
        filepath1 = mp3_to_wav(filepath1)
    if is_mp3(filepath2):
        filepath2 = mp3_to_wav(filepath2)
    #print filepath1
    #print filepath2

    data1 = read_file(filepath1)
#    array1 = string_to_array(data1, get_channel(filepath1))
#    array1 = array('h', data1)
    data2 = read_file(filepath2)
#    array2 = string_to_array(data2, get_channel(filepath2))
#    array2 = array('h', data2)

    
    cache = {}
#    fft1, fft2, powSpec1, powSpec2 = [] 
#    frate1, frate2 = 0
    if filepath1 in cache:
        fprint1 = cache[filepath1]
    else:
        #frate1 = get_frame_rate(filepath1) * 0.035
        #window = numpy.hamming(frate1)
        #print ("applied hamming for file1")
        #norm_array1 = frame_sig(array1, frate1)
        #hamWindow = apply_hamming(norm_array1, window)
        f1 = wave.open(filepath1, 'r')
        frate1 = f1.getframerate()
        nframes1 = f1.getnframes()
        f1.close()
        fprint1 = get_fprint(data1, frate1, nframes1)
        cache[filepath1] = [fprint1]

    if filepath2 in cache:
        fprint2 =  cache[filepath2]
    else:
        #frate2 = get_frame_rate(filepath2) * 0.035
        #window = numpy.hamming(frate2)
        #print ("applied hamming for file2")
        #norm_array2 = frame_sig(array2, frate2)
        #hamWindow = apply_hamming(norm_array2, window)
        f2 = wave.open(filepath2, 'r')
        frate2 = f2.getframerate()
        nframes2 = f2.getnframes()
        f2.close()
        fprint2 = get_fprint(data2, frate2, nframes2)
        cache[filepath2] = [fprint2]

    return compare_fprints(fprint1, fprint2)