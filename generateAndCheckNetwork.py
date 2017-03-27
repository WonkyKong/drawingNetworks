#!/usr/bin/env python

import sys
from lxml import objectify


class Grid:

    def __init__ (self, gridStruct):
        self.x = str (gridStruct.x).split (',')
        self.y = str (gridStruct.y).split (',')

    def to_xy (indicesStr):
        indices = str (indicesStr).split (',')
        return '{},{}'.format (self.x[indices[0]], self.y[indices[1]])

    def to_xy_array (indicesStr):
        indices = str (indicesStr).split (',')
        return [self.x[indices[0]], self.y[indices[1]]]


def createTexFile (fileName, xmlStruct):

    # This is based on the npspic class in the original Matlab code


    # Construct the grid
    grid = Grid (xmlStruct.grid)

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
