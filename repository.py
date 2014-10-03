import magic

#Checks if file is actually .wav
def check_type(file):
	mime = magic.open(magic.MIME_TYPE)
	mime.load()
	return mime.file(file)


#Tests
print check_type("audio/Sor3508.mp3")
print check_type("C:\Users\Kyle\Dropbox\Documents\Git\Sor3508.wav")
print check_type("audio/z01.wav")

