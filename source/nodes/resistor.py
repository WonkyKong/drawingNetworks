#!/usr/bin/env python

from source.nodes import Node


class subnode (Node.Node):

    def __init__ (self, nodeStruct, grid):
        super (self.__class__, self).__init__ (nodeStruct, grid)
        self.LENGTH = 0.6
        self.WIDTH = 0.2
        self.TEXT_HEIGHT = 0.3
        self.label          = self.getAttribute ('label',       '{}')
        self.orientation    = self.getAttribute ('orientation', '{}')
        if (self.orientation == None):
            self.orientation = 'h'

    def getTexString (self):
        texString = ''

        # Set the lengths according to the orientation
        if (self.orientation == 'h'):
            h1 = self.LENGTH / 2
            h2 = 0
            v1 = self.WIDTH / 2
            v2 = self.TEXT_HEIGHT
        else:
            h1 = self.WIDTH / 2
            h2 = -self.TEXT_HEIGHT
            v1 = self.LENGTH / 2
            v2 = 0

        # Draw the rectangle
        texString += '\\psframe[{}]({},{})({},{})\n'.format ('fillstyle=solid,fillcolor=white',
                                                             self.position[0] - h1,
                                                             self.position[1] - v1,
                                                             self.position[0] + h1,
                                                             self.position[1] + v1)
        # Add the text
        texString += "\\rput({},{}){{\\fontsize{{{}}}{{{}}}\\selectfont {}}}\n".format (self.position[0] + h2,
                                                                                        self.position[1] + v2,
                                                                                        8, 8, self.label)
        return texString
