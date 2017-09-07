#!/usr/bin/env python

from source.AttributeFinder import AttributeFinder
from source.Line import Line
from source.nodes import arrow


class subnode (AttributeFinder):

    def __init__ (self, nodeStruct, grid):
        AttributeFinder.__init__ (self, nodeStruct, 'node')

        text    = self.getAttribute ('text', '{}', '')
        y       = self.getAttribute ('y', '{}')
        start   = self.getAttribute ('start', '{}')
        stop    = self.getAttribute ('stop', '{}')

        startPos        = grid.to_xy_array ('{},{}'.format (start, y))
        startPosString  = '{},{}'.format (startPos[0], startPos[1])

        stopPos         = grid.to_xy_array ('{},{}'.format (stop, y))
        stopPosString   = '{},{}'.format (stopPos[0], stopPos[1])

        self.line = Line (startPosString, stopPosString, '', '')

        startX = startPos[0]
        stopX = stopPos[0]
        if startX < stopX:
            direction = 'l'
        else:
            direction = 'r'
        nodeStruct.set ('position', stopPosString)
        self.arrow = arrow.subnode (nodeStruct, grid, direction, '', '')

        textPos = grid.to_xy ('({} + {}) / 2, {} - 0.1'.format (start, stop, y))
        nodeStruct.set ('position', textPos)
        self.text = arrow.subnode (nodeStruct, grid, '', text, '')

    def getTexString (self):
        texString = ''

        texString += self.line.getTexString ()
        texString += self.arrow.getTexString ()
        texString += self.text.getTexString ()

        return texString
