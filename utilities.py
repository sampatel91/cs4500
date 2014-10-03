import sys
import subprocess

def checkArgs(args):
    if len(args) != 5:
        sys.stderr.write('ERROR: Proper command line usage is one of:\n')
        sys.stderr.write(' ./p4500 -f <pathname> -f <pathname>\n')
        sys.stderr.write(' ./p4500 -f <pathname> -d <pathname>\n')
        sys.stderr.write(' ./p4500 -d <pathname> -f <pathname>\n')
        sys.stderr.write(' ./p4500 -d <pathname> -d <pathname>\n')
        sys.exit(-1)
    else:
        if not ((args[1] == '-f' or args[1] == '-d') and
                (args[3] == '-f' or args[3] == '-d')):
          sys.stderr.write('ERROR: Proper command line usage is one of:\n')
          sys.stderr.write(' ./p4500 -f <pathname> -f <pathname>\n')
          sys.stderr.write(' ./p4500 -f <pathname> -d <pathname>\n')
          sys.stderr.write(' ./p4500 -d <pathname> -f <pathname>\n')
          sys.stderr.write(' ./p4500 -d <pathname> -d <pathname>\n')
          sys.exit(-1)

def getFileName(file):
    fileName = file.split('/')
    if len(fileName) == 0:
        return fileName
    else:
        return fileName[len(fileName) - 1]


def is_wave_file(filename):
    header_info = subprocess.Popen(
        ["file", filename], stdout=subprocess.PIPE).stdout.read()
    if (("RIFF" in header_info) and ("WAVE" in header_info)):
        return True
    else:
        return False