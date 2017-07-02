#!/usr/bin/env python

from Node import Node


class subnode (Node):

    def __init__ (self, nodeStruct, grid):
        Node.__init__ (self, nodeStruct, grid)
        self.ARM_LENGTH = 0.09
        self.RADIUS     = 0.2
        self.arrows     = self.getAttribute ('arrows', '{}')

    def getTexString (self):
        texString = ''

        # Draw the arrows
        texString += super (subnode, self).addArrows ([self.RADIUS * x for x in [-1, -1, 1, 1]], self.arrows)

        # Draw the circle
        texString += '\\pscircle[{}]({},{}){{{}}}\n'.format (
            'fillstyle=solid,fillcolor=white',
            self.position[0],
            self.position[1],
            self.RADIUS
        )

        # Draw the cross
        texString += '\\psline({},{})({},{})\n'.format (
            self.position[0]-self.ARM_LENGTH,
            self.position[1],
            self.position[0]+self.ARM_LENGTH,
            self.position[1]
        )
        texString += '\\psline({},{})({},{})\n'.format (
            self.position[0],
            self.position[1]-self.ARM_LENGTH,
            self.position[0],
            self.position[1]+self.ARM_LENGTH
        )

        return texString
