#!/usr/bin/env python

import magic, wave, scipy.fftpack

#Checks if file is actually .wav
def check_type(file):
	mime = magic.open(magic.MIME_TYPE)
	mime.load()
	return mime.file(file)


#Tests
print check_type("audio/Sor3508.mp3")
print check_type("audio/Sor3508actuallymp3.wav")
print check_type("audio/z01.wav")


z01 = wave.open('audio/z01.wav', 'r')
z02 = wave.open('audio/z02.wav', 'r')
z03 = wave.open('audio/z03.wav', 'r')

print "z01"
print z01.getsampwidth()
print z01.getframerate()
print z01.getnframes()


print "z02"
print z02.getsampwidth()
print z02.getframerate()
print z02.getnframes()

print "z03"
print z03.getsampwidth()
print z03.getframerate()
print z03.getnframes()

print scipy.fftpack.fft(z01.getframerate())
