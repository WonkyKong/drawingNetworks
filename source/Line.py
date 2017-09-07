#!/usr/bin/env python

from source.AttributeFinder import AttributeFinder

class Line (AttributeFinder):

    def __init__ (self, startPosition, endPosition, lineStyle, lineEnds):
        self.startPosition  = startPosition
        self.endPosition    = endPosition
        self.lineStyle      = lineStyle
        self.lineEnds       = lineEnds


    @classmethod
    def fromXml (cls, lineStruct, grid):
        af = AttributeFinder (lineStruct, 'line')
        startPosition   = af.getAttribute ('start',         grid.to_xy)
        endPosition     = af.getAttribute ('stop',          grid.to_xy)

        lineStyle       = af.getAttribute ('line_style',    '[{}]')
        if lineStyle == None:
            lineStyle   = af.getAttribute ('line_width',   '[linewidth={}]')
        if lineStyle == None:
            lineStyle = ''

        lineEnds       = af.isPresent ('square_ends', '', '{c-c}')
        return cls (startPosition, endPosition, lineStyle, lineEnds)

    def getTexString (self):
        return '\\psline{}{}({})({})\n'.format (
            self.lineStyle,
            self.lineEnds,
            self.startPosition,
            self.endPosition
        )
