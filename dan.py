#!/usr/bin/env python
import sys
import utilities as util
import os

def processFiles(file1, file2):
    """
    Arguments: filepath x filepath 
    
    Identifies and returns matches between two different files.
    
    This method prints:
        'MATCH ' followed by the resource files of the given file paths 
        if the resource files warrant a match.
        
        OR
        
        'NO MATCH' if the resource files of the given file paths do not match.
    """
    fileName1 = util.getFileName(file1)
    fileName2 = util.getFileName(file2)
    if (util.is_wave_file(file1) and util.is_wave_file(file2) and
    util.get_length(file1) == util.get_length(file2)):
        match_found = util.compare(file1, file2)
        if match_found:
            print "MATCH %s %s" %  (fileName1, fileName2)
        else:
            print("NO MATCH")
    else:
        print("NO MATCH")


def main(argv):
    # Check if user input is in the correct syntax
    util.checkArgs(argv)
    
    # Conditions to process and identify matching files.
    if argv[1] == '-f' and argv[3] == '-f':
        processFiles(argv[2], argv[4])
    elif argv[1] == '-f' and argv[3] == '-d':
        files = os.listdir(argv[4])
        for file in files:
            processFiles(argv[2], file)
    elif argv[1] == '-d' and argv[3] == '-f':
        files = os.listdir(argv[2])
        for file in files:
            processFiles(file, argv[4])
    elif argv[1] == '-d' and argv[3] == '-d':
        files1 = os.listdir(argv[2])
        files2 = os.listdir(argv[4])
        for file1 in files1:
            for file2 in files2:
                processFiles(file1, file2)


if __name__ == "__main__":
    main(sys.argv)

