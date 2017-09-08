#!/usr/bin/env python

from source.AttributeFinder import AttributeFinder
from source.Line import Line
from source.nodes import arrow


class subnode (AttributeFinder):

    def __init__ (self, nodeStruct, grid):
        AttributeFinder.__init__ (self, nodeStruct, 'node')

        WIDTH = 0.3
        HEIGHT = 0.3
        halfLineWidth = 0.018

        self.text   = self.getAttribute ('text', '{}')
        xString     = self.getAttribute ('x', '{}')
        yString     = self.getAttribute ('y', '{}')

        topLeftPos = grid.to_xy_array ('{},{}'.format (xString, yString))
        left    = topLeftPos[0]
        top     = topLeftPos[1]
        right   = left + WIDTH
        bottom  = top - HEIGHT

        topLeftString       = '{},{}'.format (left,                 top)
        topRightString      = '{},{}'.format (right,                top)
        bottomLeftString    = '{},{}'.format (left + halfLineWidth, bottom)
        bottomRightString   = '{},{}'.format (right,                bottom)

        self.topLine    = Line (topLeftString,      topRightString,     '', '{c-c}')
        self.rightLine  = Line (topRightString,     bottomRightString,  '', '{c-c}')
        self.bottomLine = Line (bottomRightString,  bottomLeftString,   '', '')

        nodeStruct.set ('position', bottomLeftString)
        self.arrow = arrow.subnode (nodeStruct, grid, 'r', '', '')

        self.textX = right + 0.1
        self.textY = (top + bottom) / 2

    def getTexString (self):

        texString  = self.topLine.getTexString ()
        texString += self.rightLine.getTexString ()
        texString += self.bottomLine.getTexString ()
        texString += self.arrow.getTexString ()

        texString += '\\rput[l]({},{}){{\\fontsize{{8}}{{8}}\\selectfont ${}$}}\n'.format (
            self.textX,
            self.textY,
            self.text
        )

        return texString
