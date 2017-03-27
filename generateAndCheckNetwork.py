#!/usr/bin/env python

import sys
from lxml import objectify


def createTexFile (fileName, xmlStruct):

    # This is based on the npspic class in the original Matlab code


    # Construct the grid

    # Determine the scaling
    try:
        scaleBox = xmlStruct.scaleBox
    except AttributeError:
        scaleBox = 1

    # Populate the lines

    # Populate the nodes

    # Write to the tex file
    with open (fileName, 'w') as texFile:
        texFile.write ('\\scalebox{{{}}}{{\\begin{{pspicture}}({})\n'.format (scaleBox, str (xmlStruct.picture_size).strip ()))
        # Add lines
        # Add nodes
        texFile.write ('\\end{{pspicture}}}}\n')


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
    createTexFile ("tempName.tex", xmlStruct)
