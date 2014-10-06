#!/usr/bin/env python

import magic, wave, scipy.fftpack, array
 

#Checks if file is actually .wav
def is_wave_file(file):
	mime = magic.open(magic.MIME_TYPE)
	mime.load()
	if  mime.file(file) == ('audio/x-wav'):
		return True
	else:
		return False


#Tests
print is_wave_file("audio/Sor3508.mp3")
print is_wave_file("audio/Sor3508actuallymp3.wav")
print is_wave_file("audio/z01.wav")
print is_wave_file("audio/clientMusician.mp4")

z01 = wave.open('audio/z01.wav', 'r')
z02 = wave.open('audio/z02.wav', 'r')
z07 = wave.open('audio/z07.wav', 'r')
short_test = wave.open('audio/short_test.wav', 'r')

print "z01"
print z01.getsampwidth()
print z01.getframerate()
print z01.getnframes()
print z01.getparams()
"""
print "z02"
print z02.getnchannels()
print z02.getsampwidth()
print z02.getframerate()
print z02.getnframes()
print z02.getparams()
"""
print "z07"
print z07.getnchannels()
print z07.getsampwidth()
print z07.getframerate()
print z07.getnframes()
print z07.getparams()

print "z01 frames"
frames = z01.readframes(44100)
print [ord(i) for i in frames[50:100]]
print len(frames)
print len(array.array('h', frames))
#print scipy.fftpack.fft(frames)
print "z02 frames"
frames2 =  z02.readframes(44100)
print [ord(i) for i in frames2[50:100]]
print len(frames2)
print len(array.array('h', frames2))
print "short test frames"
shortnframes =  short_test.getnframes()
frameshort = short_test.readframes(shortnframes)
print [ord(i) for i in frameshort[50:100]]
print len(frameshort)
print len(array.array('h', frameshort))
