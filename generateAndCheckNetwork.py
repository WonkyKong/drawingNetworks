#!/usr/bin/env python

import sys
from lxml import objectify


class Grid:

    def __init__ (self, gridStruct):
        self.x = str (gridStruct.x).split (',')
        self.y = str (gridStruct.y).split (',')

    def to_xy (self, indicesStr):
        indices = str (indicesStr).split (',')
        return '{},{}'.format (self.x[int (indices[0])-1].strip (),
                               self.y[int (indices[1])-1].strip ())

    def to_xy_array (self, indicesStr):
        indices = str (indicesStr).split (',')
        return [self.x[indices[0]], self.y[indices[1]]]


class Line:

    def __init__ (self, lineStruct, grid):
        self.startPosition  = grid.to_xy (str (lineStruct.start).strip ())
        self.endPosition    = grid.to_xy (str (lineStruct.stop).strip ())
        try:
            self.lineStyle = '[linewidth={}]'.format (lineStruct.line_width.strip ())
        except AttributeError:
            try:
                self.lineStyle = '[{}]'.format (lineStruct.line_style.strip ())
            except AttributeError:
                self.lineStyle = ''
        if (hasattr (lineStruct, 'square_ends')):
            self.lineEnds = ''
        else:
            self.lineEnds = '{c-c}'

    def getTexString (self):
        return '\\psline{}{}({})({})\n'.format (self.lineStyle,
                                                  self.lineEnds,
                                                  self.startPosition,
                                                  self.endPosition)



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
    lines = []
    for xmlLine in xmlStruct.lines.line:
        lines.append (Line (xmlLine, grid))

    # Populate the nodes

    # Write to the tex file
    with open (fileName, 'w') as texFile:
        texFile.write ('\\scalebox{{{}}}{{\\begin{{pspicture}}({})\n'.format (scaleBox, str (xmlStruct.picture_size).strip ()))

        # Add lines
        for line in lines:
            texFile.write (line.getTexString ())

        # Add nodes

        texFile.write ('\\end{pspicture}}\n')


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
