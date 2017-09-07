#!/usr/bin/env python

from source.AttributeFinder import AttributeFinder
from source.Line import Line
from source.nodes import rectangle


class subnode (AttributeFinder):

    def __init__ (self, nodeStruct, grid):
        AttributeFinder.__init__ (self, nodeStruct, 'node')

        text    = self.getAttribute ('text', '{}')
        colour  = self.getAttribute ('colour', '{}')
        x       = self.getAttribute ('x', '{}')
        start   = self.getAttribute ('start', '{}')
        stop    = self.getAttribute ('stop', '{}')
        width   = self.getAttribute ('width', float)

        startPos        = grid.to_xy_array ('{},{}'.format (x, start))
        startPosString  = '{},{}'.format (startPos[0], startPos[1])

        stopPos         = grid.to_xy_array ('{},{}'.format (x, stop))
        stopPosString   = '{},{}'.format (stopPos[0], stopPos[1])

        if colour == None:
            lineColour = 'black'
            frameFormat = 'fillstyle=solid,fillcolor=white'
        else:
            lineColour = colour
            frameFormat = 'fillstyle=solid,fillcolor={},opacity=0.5,linecolor={}'.format (colour, colour)

        lineStyle = '[linestyle=dashed,dash=3pt 2pt,linecolor={}]'.format (lineColour)
        self.line = Line (startPosString, stopPosString, lineStyle, '')

        nodeStruct.set ('position', startPosString)
        self.rectangle = rectangle.subnode (nodeStruct, grid, 0.6, width, "top",
            frameFormat, True, text, 'middle')

    def getTexString (self):
        texString = ''

        texString += self.line.getTexString ()
        texString += self.rectangle.getTexString ()

        return texString
