#!/usr/bin/env python

import imp
import os
import re
import sys
from contextlib import contextmanager
from lxml import objectify
import subprocess

from source.AttributeFinder import AttributeFinder



class Grid (AttributeFinder):

    def __init__ (self, gridStruct, constantsDict):
        AttributeFinder.__init__ (self, gridStruct, 'grid')

        def splitValues (s):
            return  [element.strip () for element in s.split (',')]

        def isNumber (s):
            try:
                float (s)
                return True
            except ValueError:
                return False

        self.x = self.getAttribute ('x', splitValues)
        i = 0
        for x in self.x:
            if not isNumber (x):
                try:
                    self.x[i] = '{}'.format (constantsDict[x])
                except:
                    print "Unknown constant"
            i = i + 1

        self.y = self.getAttribute ('y', splitValues)
        i = 0
        for y in self.y:
            if not isNumber (y):
                try:
                    self.y[i] = '{}'.format (constantsDict[y])
                except:
                    print "Unknown constant"
            i = i + 1

    def to_xy (self, indicesStr):
        indices = str (indicesStr).split (',')
        return '{},{}'.format (self.x[int (indices[0]) - 1].strip (),
                               self.y[int (indices[1]) - 1].strip ())

    def to_xy_array (self, indicesStr):
        indices = str (indicesStr).split (',')
        return [float (self.x[int (indices[0]) - 1]),
                float (self.y[int (indices[1]) - 1])]


def getNodeType (nodeStruct):

    type = nodeStruct.tag
    if type == "node":
        # Try getting the type from an attribute
        type = nodeStruct.get ("type")
        if type is None:
            # Get the type from a sub-node
            type = str (nodeStruct.type).strip ()
    return type


class Line (AttributeFinder):

    def __init__ (self, lineStruct, grid):
        AttributeFinder.__init__ (self, lineStruct, 'line')
        self.startPosition  = self.getAttribute ('start',        grid.to_xy)
        self.endPosition    = self.getAttribute ('stop',         grid.to_xy)

        self.lineStyle      = self.getAttribute ('line_style',   '[{}]')
        if self.lineStyle == None:
            self.lineStyle  = self.getAttribute ('line_width',   '[linewidth={}]')
        if self.lineStyle == None:
            self.lineStyle = ''

        self.lineEnds       = self.isPresent ('square_ends', '', '{c-c}')

    def getTexString (self):
        return '\\psline{}{}({})({})\n'.format (
            self.lineStyle,
            self.lineEnds,
            self.startPosition,
            self.endPosition
        )


class Constant (AttributeFinder):
    def __init__ (self, xmlConstant, constantsDict):
        AttributeFinder.__init__ (self, xmlConstant, 'constant')

        # Get the expression string
        expression = self.getAttribute ('expression', '{}')
        if expression != None:

            # Make a set of the words
            wordSet = filter (lambda x:re.match("^[a-zA-Z]+$",x),[x for x in set(re.split("[\s:/,.:]",expression))])

            # Replace each word in the expression string with a reference into the constants dictionary
            for word in wordSet:
                expression = re.sub (r'\b' + re.escape (word) + r'\b', 'constantsDict["{}"]'.format (word), expression)

            # Evaluate the expression string
            exec (expression) in locals ()


def createTexFile (fileName, xmlStruct):

    # Get any constants
    constantsDict = {}
    for xmlConstant in xmlStruct.constants.constant:
        Constant (xmlConstant, constantsDict)

    # Construct the grid
    grid = Grid (xmlStruct.grid, constantsDict)

    # Determine the scaling
    try:
        scaleBox = xmlStruct.scaleBox
    except AttributeError:
        scaleBox = 1

    # Populate the lines
    lines = []
    for xmlLine in xmlStruct.lines.line:
        lines.append (Line (xmlLine, grid))

    # Load the node modules
    nodeModules = {}
    for xmlNode in xmlStruct.nodes.getchildren ():
        if xmlNode.tag != "comment":
            type = getNodeType (xmlNode)
            if type not in nodeModules:
                try:
                    nodeModules[type] = imp.load_source (type, 'source/nodes/{}.py'.format (type))
                except:
                    print "source/nodes/{}.py not found".format (type)

    # Populate the nodes
    nodes = []
    for xmlNode in xmlStruct.nodes.getchildren ():
        if xmlNode.tag != "comment":
            type = getNodeType (xmlNode)
            newNode = nodeModules[type].subnode (xmlNode, grid)
            nodes.append (newNode)

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
    (path, filename) = os.path.split (texFileName)
    wrapperFileName = os.path.join (path, 'wrapper_' + filename)
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
    texContents += filename
    texContents += """}
        }
    \end{figure}
\end{document}
"""
    with open (wrapperFileName, 'w') as wrapperFile:
        wrapperFile.write (texContents)

@contextmanager
def pushd (newDir):
    previousDir = os.getcwd ()
    os.chdir (newDir)
    yield
    os.chdir (previousDir)


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
    (path, stem) = os.path.split (fileNameStem)
    if not path:
        path = "."
    wrapperStem = 'wrapper_' + stem
    with pushd (path):
        FNULL = open(os.devnull, 'w')
        subprocess.call (['/Library/TeX/texbin/latex', wrapperStem + '.tex'], stdout=FNULL)
        subprocess.call (['/Library/TeX/texbin/dvips', '-Ppdf', '-t', 'a$', wrapperStem, '-o'], stdout=FNULL, stderr=FNULL)
        subprocess.call (['ps2pdf', wrapperStem + '.ps', wrapperStem + '.pdf'], stdout=FNULL)
        FNULL.close ()
