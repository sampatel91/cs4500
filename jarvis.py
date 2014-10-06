#!/usr/bin/env python
import sys
import utilities as util
import os

def processFiles(file1, file2):
    fileName1 = util.getFileName(file1)
    fileName2 = util.getFileName(file2)
    if (util.is_wave_file(fileName1) and util.is_wave_file(fileName2) and
    util.get_length(fileName1) == util.get_length(fileName2)):
        match_found = util.compare(fileName2, fileName2)
        if match_found:
            print("MATCH %s %s", file1, file2)
        else:
            print("NO MATCH FOUND")
    else:
        print("NO MATCH FOUND")


def main(argv):
    util.checkArgs(argv)
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

