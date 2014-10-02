
import sys, wave, struct, math, subprocess, os
import numpy as np
from scipy.fftpack import dct


def main(file1, file2):
	sys.exit(0)
    




def parseArgs(args):

 if args[1] == '-f' and args[3] == '-f':
 	main(argv[2], argv[4])
 	sys.exit(0)



if __name__ == '__main__':

	if len(sys.argv) != 5:
	 	sys.stderr.write('ERROR: Proper command line usage is one of:\n')
	 	sys.exit(-1)	
	else:
    	 if not (sys.argv[1] == '-f' or sys.argv[3] == '-f'):
    	 	sys.stderr.write('ERROR: Proper command line usage is one of:\n')
         	sys.stderr.write(' ./p4500 -f <pathname> -f <pathname>\n')
         	sys.exit(-1)
    	 else:
    	 	parseArgs(sys.argv)