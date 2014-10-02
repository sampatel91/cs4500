
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      marcs
#
# Created:     02/10/2014
# Copyright:   (c) marcs 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/python -B



import os, sys

def validate_command():
    """Validates the commands.

    Prints an stderror if the commands are invalid.

    Returns:
        TRUE if the arguments are correct; otherwise FALSE.
    """

    valid_args = (len(sys.argv) == 5 and
                    ((sys.argv[1] == '-f' and os.path.isfile(sys.argv[2]))
                    or (sys.argv[1] == '-d' and os.path.isdir(sys.argv[2])))
                    and
                    ((sys.argv[3] == '-f' and os.path.isfile(sys.argv[4]))
                    or (sys.argv[3] == '-d' and os.path.isdir(sys.argv[4]))))

    error_list = ['Error {0} -f <path> -f <path>\n',
                  'Error {0} -f <path> -d <path>\n',
                  'Error {0} -d <path> -f <path>\n'
                  'Error {0} -d <path> -d <path>\n']

    if not valid_args:
        sys.stderr.write('Error: one of \n')
        sys.stderr.writelines([str.format(sys.argv[0]) for e in error_list])
        return False
    return True

def main():
    if not validate_command():
        sys.stdout.write('This works! SICK\n')

if __name__ == '__main__':
    main()