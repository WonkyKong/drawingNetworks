#!/usr/bin/env python

import sys
from lxml import objectify


if __name__ == "__main__":

    # Check that have at least one argument
    if (len (sys.argv) < 2):
        print "Must supply the name of an XML file."
        sys.exit (-1)


    # Get XML file
    try:
        with open (sys.argv[1], 'r') as xmlFile:
            xmlString = xmlFile.read ().replace ('\n', '')
    except NameError:
        print "Unable to read the XML file."
        sys.exit (-1)
    xmlStruct = objectify.fromstring (xmlString)


    # Generate tex file
