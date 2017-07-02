#!/usr/bin/env python

import unittest
import os
from contextlib import contextmanager
from subprocess import call

@contextmanager
def pushd (newDir):
    previousDir = os.getcwd ()
    os.chdir (newDir)
    yield
    os.chdir (previousDir)

class CurrentDirectForm1Generation (unittest.TestCase):
    def test_current_DirectForm1_XML (self):
        # Go to the directory containing generateAndCheckNetwork.py ...
        with pushd (os.path.dirname (os.path.dirname (os.path.realpath (__file__)))):
            # ... and run generateAndCheckNetwork.py on the DirectForm1 XML file
            call (['./generateAndCheckNetwork.py', 'exampleXML/DirectForm1.XML'])
            # Check this matches the original version of the generated tex file
            self.assertTrue (open ('exampleXML/DirectForm1.tex', 'rb').read() == open('tests/expectedTex/DirectForm1.tex', 'rb').read())

if __name__ == "__main__":
    unittest.main ()
