#!/usr/bin/env python

import os
from contextlib import contextmanager
from subprocess import call

@contextmanager
def pushd (newDir):
    previousDir = os.getcwd ()
    os.chdir (newDir)
    yield
    os.chdir (previousDir)

if __name__ == "__main__":
    with pushd (os.path.dirname (os.path.dirname (os.path.realpath (__file__)))):
        call (['./generateAndCheckNetwork.py', 'DirectForm1.XML'])
        print open('DirectForm1.tex', 'rb').read() == open('tests/DirectForm1.tex', 'rb').read()
