#!/usr/bin/env python

import magic

#Checks if file is actually .wav
def check_type(file):
	mime = magic.open(magic.MIME_TYPE)
	mime.load()
	return mime.file(file)


#Tests
print check_type("audio/Sor3508.mp3")
print check_type("audio/Sor3508actuallymp3.wav")
print check_type("audio/z01.wav")

