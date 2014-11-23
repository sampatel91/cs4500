import numpy
from operator import itemgetter
import wave

def get_fft(signal):
    """
    Arguments: audio signal

    Applies, computes, and returns the Fast Fourier Transform
    of the given audio signal.  
    """
    ffts =[]
    fft = numpy.fft.fft(signal)
    for sample in fft:
        x = abs(sample)
        ffts.append(x)
    return ffts

def get_peak(ffts):
    """
    Arguments: the spectral data returned by the FFT Algorithm.

    Returns the highest spectral value found in the FFT data.
    """
    return max(enumerate(ffts), key=itemgetter(1))[0]

def get_fprint(data, frate, nframes, chunk_size):
    """
    Arguments: array of integers x frame rate x number of frames x size of
    chunk.

    Returns the fingerprint result that contains the peak values of an audio
    file.
    """
    result = []
    for i in range(0, nframes, chunk_size):
        chunk_data = data[i:i+chunk_size]
        ffts = get_fft(chunk_data)
        peak_val = get_peak(ffts)
        result.append(peak_val)
    return result

