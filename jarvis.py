#!/usr/bin/python
import sys
import utilities
import os

def processFiles(file1, file2):
    fileName1 = utilities.getFileName(file1)
    fileName2 = utilities.getFileName(file2)

def main(argv):
    utilities.checkArgs(argv)
    if argv[1] == '-f' and argv[3] == '-f':
        processFiles(argv[1], argv[3])
    elif argv[1] == '-f' and argv[3] == '-d':
        files = os.listdir(argv[3])
        for file in files:
            processFiles(argv[1], file)
    elif argv[1] == '-d' and argv[3] == '-f':
        files = os.listdir(argv[1])
        for file in files:
            processFiles(file, argv[3])
    elif argv[1] == '-d' and argv[3] == '-d':
        files1 = os.listdir(argv[1])
        files2 = os.listdir(argv[3])
        for file1 in files1:
            for file2 in files2:
                processFiles(file1, file2)


if __name__ == "__main__":
    main(sys.argv)

