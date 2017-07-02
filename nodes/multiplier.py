#!/usr/bin/env python

from nodes import Node


class subnode (Node.Node):

    def __init__ (self, nodeStruct, grid):
        super (self.__class__, self).__init__ (nodeStruct, grid)
        self.TRI_HEIGHT     = 0.5
        self.TRI_LENGTH     = 0.6
        self.TEXT_HEIGHT    = 0.45
        self.direction      = self.getAttribute ('direction',   '{}')
        self.coefficient    = self.getAttribute ('coefficient', '{}')
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
        texString += super (subnode, self).addArrows ([self.TRI_LENGTH * 0.5 * x for x in [-1, -1, 1, 1]], self.direction)

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
