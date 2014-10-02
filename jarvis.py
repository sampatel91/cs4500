#!/usr/bin/python
import sys
from argparse import ArgumentParser

def main(argv):
    parser = ArgumentParser(
        usage="%(prog)s [option] <pathname> [option] <pathname>")
    print (argv)


if __name__ == "__main__":
    main(sys.argv)

