#!/usr/bin/env python

import os
import sys
from lxml import objectify
from subprocess import call


class Grid:

    def __init__ (self, gridStruct):
        self.x = str (gridStruct.x).split (',')
        self.y = str (gridStruct.y).split (',')

    def to_xy (self, indicesStr):
        indices = str (indicesStr).split (',')
        return '{},{}'.format (self.x[int (indices[0]) - 1].strip (),
                               self.y[int (indices[1]) - 1].strip ())

    def to_xy_array (self, indicesStr):
        indices = str (indicesStr).split (',')
        return [float (self.x[int (indices[0]) - 1]),
                float (self.y[int (indices[1]) - 1])]


class Node (object):

    def __init__ (self, nodeStruct, grid):
        self.position = grid.to_xy_array (nodeStruct.position)
        self.ARROW_LENGTH   = 0.09
        self.ARROW_NUDGE    = 0.02

    def __leftArrow (self, shapeLimits):
        ex = self.position[0] + shapeLimits[0] + self.ARROW_NUDGE
        sx = ex - self.ARROW_LENGTH
        ey = self.position[1]
        sy = ey
        return [ex, sx, ey, sy]

    def __bottomArrow (self, shapeLimits):
        ex = self.position [0]
        sx = ex
        ey = self.position [1] + shapeLimits [1] + self.ARROW_NUDGE
        sy = ey - self.ARROW_LENGTH
        return [ex, sx, ey, sy]

    def __rightArrow (self, shapeLimits):
        ex = self.position[0] + shapeLimits[2] - self.ARROW_NUDGE
        sx = ex + self.ARROW_LENGTH
        ey = self.position[1]
        sy = ey
        return [ex, sx, ey, sy]

    def __topArrow (self, shapeLimits):
        ex = self.position [0]
        sx = ex
        ey = self.position [1] + shapeLimits [3] - self.ARROW_NUDGE
        sy = ey + self.ARROW_LENGTH
        return [ex, sx, ey, sy]

    def addArrows (self, shapeLimits, arrows):
        returnString = ''
        for arrow in arrows:
            [ex,sx,ey,sy] = {
                'l': self.__leftArrow   (shapeLimits),
                'b': self.__bottomArrow (shapeLimits),
                'r': self.__rightArrow  (shapeLimits),
                't': self.__topArrow    (shapeLimits),
            }[str (arrow).strip ()]
            returnString += '\\psline[{}]({},{})({},{})\n'.format ('linecolor=white,linewidth=2pt', sx, sy, ex, ey)
            returnString += '\\psline[{}]({},{})({},{})\n'.format ('arrowinset=0,arrows=->', sx, sy, ex, ey)
        return returnString

    def getTexString (self):
        return ''


class Multiplier (Node):

    def __init__ (self, nodeStruct, grid):
        Node.__init__ (self, nodeStruct, grid)
        self.TRI_HEIGHT     = 0.5
        self.TRI_LENGTH     = 0.6
        self.TEXT_HEIGHT    = 0.45
        self.direction      = str (nodeStruct.direction).strip ()
        self.coefficient    = str (nodeStruct.coefficient).strip ()
        self.triangle       = [ [-self.TRI_LENGTH / 2,   self.TRI_HEIGHT / 2],
                                [-self.TRI_LENGTH / 2,  -self.TRI_HEIGHT / 2],
                                [ self.TRI_LENGTH / 2,   0]]

    def __getTriangleCoordinates (self):
        tri = self.triangle

        # Reverse the triangle if coming from right or bottom
        # (negate the x coordinates)
        if ((self.direction == 'r') or (self.direction == 't')):
            tri = [[-x[0], x[1]] for x in tri]

        # Swap the x and y coordinates if the multiplier is vertical
        if ((self.direction == 'b') or (self.direction == 't')):
            tri = [[x[1], x[0]] for x in tri]

        # Return the string with the coordinates
        coordinateString = ''
        for pair in tri:
            coordinateString += '({},{})'.format (pair[0] + self.position[0],
                                                  pair[1] + self.position[1])
        return coordinateString

    def getTexString (self):
        texString = ''

        # Draw the arrows
        texString += super (Multiplier, self).addArrows ([self.TRI_LENGTH * 0.5 * x for x in [-1, -1, 1, 1]], self.direction)

        # Draw the triangle
        texString += '\\pspolygon[fillstyle=solid,fillcolor=white]{}\n'.format (self.__getTriangleCoordinates ())

        # Set the lengths according to the orientation
        if ((self.direction == 'b') or (self.direction == 't')):
            h1 = self.TEXT_HEIGHT
            v1 = 0
        else:
            h1 = 0
            v1 = self.TEXT_HEIGHT

        # Add the coefficient
        texString += '\\rput({},{}){{\\fontsize{{8}}{{8}}\\selectfont ${}$}}\n'.format (self.position[0]+h1,
                                                                                  self.position[1]+v1,
                                                                                  self.coefficient)

        return texString


def NodeFactory (nodeStruct, grid):
    type = str (nodeStruct.type).strip ()
    if type == 'multiplier': return Multiplier (nodeStruct, grid)
    return Node (nodeStruct, grid)


class Line:

    def __init__ (self, lineStruct, grid):
        self.startPosition  = grid.to_xy (str (lineStruct.start).strip ())
        self.endPosition    = grid.to_xy (str (lineStruct.stop).strip ())
        find = objectify.ObjectPath ("line.line_style")
        try:
            self.lineStyle = '[{}]'.format (find (lineStruct).text.strip ())
        except:
            find = objectify.ObjectPath ("line.line_width")
            try:
                self.lineStyle = '[linewidth={}]'.format (find (lineStruct).strip ())
            except:
                self.lineStyle = ''

        find = objectify.ObjectPath ("line.square_ends")
        try:
            square_ends = find (lineStruct).tag
            self.lineEnds = ''
        except:
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
    nodes = []
    for xmlNode in xmlStruct.nodes.node:
        nodes.append (NodeFactory (xmlNode, grid))

    # Write to the tex file
    with open (fileName, 'w') as texFile:
        texFile.write ('\\scalebox{{{}}}{{\\begin{{pspicture}}({})\n'.format (scaleBox, str (xmlStruct.picture_size).strip ()))

        # Add lines to the tex file
        for line in lines:
            texFile.write (line.getTexString ())

        # Add nodes to the tex file
        for node in nodes:
            texFile.write (node.getTexString ())

        texFile.write ('\\end{pspicture}}\n')


def createWrapperTexFile (texFileName):
    wrapperFileName = 'wrapper_' + texFileName
    texContents = """\
\documentclass[fleqn,12pt]{article}
\usepackage[rmargin=1in,lmargin=1in,tmargin=0.7in,bmargin=1in]{geometry}
\usepackage{graphicx}
\usepackage{verbatim}
\usepackage{amsmath}
\usepackage{chngpage}
\usepackage{multirow}
\usepackage{amsfonts}
\usepackage{amsmath}
\usepackage{mathrsfs}
\usepackage{hyperref}
\usepackage{comment}
\usepackage{rotating}
\usepackage{color}
\usepackage{array}
\usepackage{colortbl}
\usepackage{pst-all}
\usepackage{epstopdf}
\usepackage{auto-pst-pdf}
\\begin{document}
    \\begin{figure}[!ht]
        \centerline{
            \input{"""
    texContents += texFileName
    texContents += """}
        }
    \end{figure}
\end{document}
"""
    with open (wrapperFileName, 'w') as wrapperFile:
        wrapperFile.write (texContents)


if __name__ == "__main__":

    # Check that have at least one argument
    if (len (sys.argv) < 2):
        print "Must supply the name of an XML file."
        sys.exit (-1)

    # Get XML file
    xmlFileName = sys.argv[1]
    try:
        with open (xmlFileName, 'r') as xmlFile:
            xmlString = xmlFile.read ().replace ('\n', '')
    except NameError:
        print "Unable to read the XML file."
        sys.exit (-1)
    xmlStruct = objectify.fromstring (xmlString)

    # Generate tex file
    fileNameStem = os.path.splitext (xmlFileName)[0]
    texFileName = fileNameStem + '.tex'
    createTexFile (texFileName, xmlStruct)

    # Generate the wrapper tex file
    createWrapperTexFile (texFileName)

    # Generate the pdf
    wrapperStem = 'wrapper_{}'.format (fileNameStem)
    call (['/Library/TeX/texbin/latex', wrapperStem + '.tex'])
    call (['/Library/TeX/texbin/dvips', '-Ppdf', '-t', 'a$', wrapperStem, '-o'])
    call (['ps2pdf', wrapperStem + '.ps', wrapperStem + '.pdf'])
