#!/usr/bin/env python

from source.AttributeFinder import AttributeFinder

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
