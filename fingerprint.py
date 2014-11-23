import numpy
from operator import itemgetter
import wave
import scipy.io.wavfile

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
    #weight = 20
    chunk_size = frate/ 10
    for i in range(0, nframes, chunk_size):
        chunk_data = data[i:i+chunk_size]
        ffts = get_fft(chunk_data)
        #peak_val = get_peak(ffts) * frate / len(chunk_data) 
	#weight = frate/chunk_size
        peak_val = get_peak(ffts)
        #weight -= 1
        result.append(peak_val)
    return result

