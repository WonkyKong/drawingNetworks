#!/usr/bin/env python

from source.AttributeFinder import AttributeFinder


class Node (object, AttributeFinder):

    def __init__ (self, nodeStruct, grid):
        AttributeFinder.__init__ (self, nodeStruct, 'node')
        self.position = self.getAttribute ('position', grid.to_xy_array)
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
