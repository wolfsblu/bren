#!/bin/env python3

import argparse
import fileinput

from gui import GUI
from renamer import Renamer
from os.path import isfile


def main():
    parser = argparse.ArgumentParser(description='Rename some files.')
    parser.add_argument('files', help='file containing list of file names to rename')
    args = parser.parse_args()

    with fileinput.input(files=(args.files,)) as f:
        files = [l.rstrip() for l in f if isfile(l.rstrip())]

    renamer = Renamer(files)

if __name__ == '__main__':
    main()
